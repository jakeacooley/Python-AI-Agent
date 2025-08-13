from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

# get_files_info tests

# get_file_result1 = get_files_info("calculator", ".")
# print("Result for current directory:")
# print(get_file_result1)

# get_file_result2 = get_files_info("calculator", "pkg")
# print("Result for 'pkg' directory:")
# print(get_file_result2)

# get_file_result3 = get_files_info("calculator", "/bin")
# print("Result for '/bin' directory:")
# print(get_file_result3)

# get_file_result4 = get_files_info("calculator", "../")
# print("Result for '../' directory:")
# print(get_file_result4)


# get_file_content tests

# file_content_1 = get_file_content("calculator", "main.py")
# print(f"Content: {file_content_1}")

# file_content_2 = get_file_content("calculator", "pkg/calculator.py")
# print(f"Content: {file_content_2}")

# file_content_3 = get_file_content("calculator", "/bin/cat")
# print(f"Content: {file_content_3}")

# file_content_4 = get_file_content("calculator", "pkg/does_not_exist.py")
# print(f"Content: {file_content_4}")


# write_file tests

# write_file_result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(write_file_result1)

# write_file_result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(write_file_result2)

# write_file_result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(write_file_result3)


# run_python tests

run_python_result1 = run_python_file("calculator", "main.py") # (should print the calculator's usage instructions)
print(run_python_result1)

run_python_result2 = run_python_file("calculator", "main.py", ["3 + 5"]) # (should run the calculator... which gives a kinda nasty rendered result)
print(run_python_result2)

run_python_result3 = run_python_file("calculator", "tests.py")
print(run_python_result3)

run_python_result4 = run_python_file("calculator", "../main.py") # (this should return an error)
print(run_python_result4)

run_python_result5 = run_python_file("calculator", "nonexistent.py") # (this should return an error)
print(run_python_result5)
