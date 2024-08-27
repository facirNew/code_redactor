import subprocess

from testcases import case, expected_result

for idx, el in enumerate(case):
    input_data = el.replace(', ', '\n')
    result = subprocess.run(args=['python', 'code.py'],
                            input=input_data,
                            timeout=3,
                            check=False,
                            capture_output=True,
                            text=True,
                            )
    if result.stderr:
        print(result.stderr)  # noqa: T201
        break
    if result.stdout.strip() != str(expected_result[idx]):
        print(f'error in test {idx + 1}: '  # noqa: T201
              f'input data: {el} '
              f'you result: {result.stdout.strip()} '
              f'excepted result: {expected_result[idx]!s}')
        break
