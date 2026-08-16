import pathlib
import sys
import zipfile


def validate_wheel(path):
    if path.name.endswith('-none-any.whl'):
        raise RuntimeError(f'pure-Python wheel tag found: {path.name}')

    with zipfile.ZipFile(path) as wheel:
        names = wheel.namelist()
        metadata_names = [name for name in names if name.endswith('.dist-info/WHEEL')]
        native_names = [
            name for name in names if name.endswith(('.pyd', '.so', '.dylib'))
        ]
        if len(metadata_names) != 1:
            raise RuntimeError(f'expected one WHEEL metadata file in {path.name}')
        if not native_names:
            raise RuntimeError(f'no native extension found in {path.name}')

        metadata = wheel.read(metadata_names[0]).decode('utf-8')
        if 'Root-Is-Purelib: false' not in metadata:
            raise RuntimeError(f'wheel is marked pure: {path.name}')

        tags = [line[5:] for line in metadata.splitlines() if line.startswith('Tag: ')]
        if not tags or any(tag.endswith('-any') for tag in tags):
            raise RuntimeError(f'non-platform wheel metadata tag found in {path.name}: {tags}')

    tag_list = ', '.join(tags)
    print(f'{path.name}: native={native_names[0]}, tags={tag_list}')


def main():
    distribution_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
    sdists = sorted(distribution_dir.glob('*.tar.gz'))
    wheels = sorted(distribution_dir.glob('*.whl'))

    if len(sdists) != 1:
        raise RuntimeError(f'expected one sdist, found {len(sdists)}')
    if not wheels:
        raise RuntimeError('no wheels found')

    print(f'source distribution: {sdists[0].name}')
    for wheel in wheels:
        validate_wheel(wheel)


if __name__ == '__main__':
    main()
