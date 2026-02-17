from config import MAX_CHARS
from functions.get_file_content import get_file_content


result = get_file_content("calculator", "lorem.txt")
print(f"Length of result: {len(result)}")
print(f"Truncated: {result.endswith(f'[...File \"lorem.txt\" truncated at {MAX_CHARS} characters]')}")
print(f"Last 100 chars: ...{result[-100:]}")

print()
result = get_file_content("calculator", "main.py")
print("Result for 'main.py':")
print(result)

print()
result = get_file_content("calculator", "pkg/calculator.py")
print("Result for 'pkg/calculator.py':")
print(result)

print()
result = get_file_content("calculator", "/bin/cat")
print("Result for '/bin/cat':")
print(f"  {result}")

print()
result = get_file_content("calculator", "pkg/does_not_exist.py")
print("Result for 'pkg/does_not_exist.py':")
print(f"  {result}")
