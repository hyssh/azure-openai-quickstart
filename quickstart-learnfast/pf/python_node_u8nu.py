
from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str, input2: str, input3: str) -> str:
    if input1 is not None:
        return input1
    elif input2 is not None:
        return input2
    else:
        return input3
