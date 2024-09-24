import io
import zipfile
import gzip


def unzip(zip_bytes: bytes) -> bytes:
    stream = io.BytesIO(zip_bytes)

    with zipfile.ZipFile(stream, "r") as zip:
        file_name = zip.namelist()[0]  # We only have one file every time

        with zip.open(file_name) as f:
            file_bytes = f.read()

    return file_bytes


def ungzip(gzip_bytes: bytes) -> bytes:
    gzip.decompress(gzip_bytes)
