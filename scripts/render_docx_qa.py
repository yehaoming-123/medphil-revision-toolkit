import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def build_soffice_command(input_path, output_dir, profile_dir, soffice="soffice"):
    profile_uri = Path(profile_dir).resolve().as_uri()
    return [
        str(soffice),
        "-env:InstallMode=",
        f"-env:UserInstallation={profile_uri}",
        "--headless",
        "--norestore",
        "--convert-to",
        "pdf",
        "--outdir",
        str(Path(output_dir).resolve()),
        str(Path(input_path).resolve()),
    ]


def _find_executable(explicit, names, common_paths=()):
    if explicit:
        candidate = Path(explicit)
        if candidate.is_file():
            return str(candidate)
        resolved = shutil.which(explicit)
        if resolved:
            return resolved
        raise FileNotFoundError(f"executable not found: {explicit}")
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    for path in common_paths:
        if Path(path).is_file():
            return str(path)
    raise FileNotFoundError(f"none of these executables were found: {', '.join(names)}")


def render_docx_qa(
    input_path,
    output_dir,
    soffice=None,
    pdftoppm=None,
    dpi=160,
    emit_pdf=True,
):
    source = Path(input_path)
    output = Path(output_dir)
    if source.suffix.casefold() != ".docx" or not source.is_file():
        raise ValueError("input must be an existing DOCX")
    if output.exists():
        raise FileExistsError(f"render output already exists: {output.resolve()}")
    office = _find_executable(
        soffice,
        ("soffice.com", "soffice"),
        (r"C:\Program Files\LibreOffice\program\soffice.com",),
    )
    rasterizer = _find_executable(
        pdftoppm,
        ("pdftoppm", "pdftoppm.exe"),
        (
            Path.home()
            / ".cache"
            / "codex-runtimes"
            / "codex-primary-runtime"
            / "dependencies"
            / "native"
            / "poppler"
            / "Library"
            / "bin"
            / "pdftoppm.exe",
        ),
    )

    output.mkdir(parents=True)
    try:
        with tempfile.TemporaryDirectory(prefix="medphil_soffice_profile_") as profile:
            with tempfile.TemporaryDirectory(prefix="medphil_soffice_convert_") as conversion:
                command = build_soffice_command(source, conversion, profile, office)
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                )
                pdf = Path(conversion) / f"{source.stem}.pdf"
                if result.returncode != 0 or not pdf.is_file():
                    raise RuntimeError(
                        "LibreOffice conversion failed: "
                        f"exit={result.returncode}\n{result.stdout}\n{result.stderr}"
                    )
                if emit_pdf:
                    shutil.copy2(pdf, output / pdf.name)
                raster = subprocess.run(
                    [
                        rasterizer,
                        "-png",
                        "-r",
                        str(int(dpi)),
                        str(pdf),
                        str(output / "page"),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                )
                if raster.returncode != 0:
                    raise RuntimeError(
                        "PDF rasterization failed: "
                        f"exit={raster.returncode}\n{raster.stdout}\n{raster.stderr}"
                    )
        pages = sorted(output.glob("page-*.png"))
        if not pages or any(path.stat().st_size == 0 for path in pages):
            raise RuntimeError("rasterization produced no valid PNG pages")
        return pages
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output_dir")
    parser.add_argument("--soffice")
    parser.add_argument("--pdftoppm")
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--no-pdf", action="store_true")
    args = parser.parse_args()
    pages = render_docx_qa(
        args.input,
        args.output_dir,
        soffice=args.soffice,
        pdftoppm=args.pdftoppm,
        dpi=args.dpi,
        emit_pdf=not args.no_pdf,
    )
    print(f"Rendered {len(pages)} page(s) to {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
