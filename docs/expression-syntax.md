# Expression Language Documentation

## Overview

This documentation provides a comprehensive guide to building expressions using the custom expression language. This language is designed to evaluate criteria against host variables and group variables, making it suitable for use in environments like Ansible for dynamic inventory generation.

## Table of Contents

1. [Introduction](#introduction)
2. [Token Types](#token-types)
3. [Operators](#operators)
4. [Syntax](#syntax)
5. [Examples](#examples)
6. [Evaluation Process](#evaluation-process)
7. [Debugging](#debugging)

## Introduction

Expressions are built using variables, constants, and operators to form logical and comparison statements. These expressions are then evaluated to determine if they meet certain criteria.

## Token Types

Tokens are the basic building blocks of expressions. There are several types of tokens:

- **VARIABLE**: Represents a variable name, e.g., `app`, `type`.
- **COMPARISON_OPERATOR**: Represents comparison operators, e.g., `=`, `!=`.
- **UNARY_OPERATOR**: Represents unary operators, e.g., `ISNULL`, `GTZ`.
- **CONSTANT**: Represents a constant value, e.g., `"proxmox"`, `10`.
- **LOGICAL_OPERATOR**: Represents logical operators, e.g., `AND`, `OR`.
- **GROUPING_START**: Represents the start of a grouping, e.g., `(`.
- **GROUPING_END**: Represents the end of a grouping, e.g., `)`.

## Operators

Operators are used to perform operations on variables and constants. They are divided into comparison and unary operators.

### Comparison Operators

| Operator          | Symbols                       | Description                                  |
|-------------------|-------------------------------|----------------------------------------------|
| EQUAL             | `=`, `==`, `EQUALS`           | Checks if two values are equal               |
| NOT_EQUAL         | `!=`, `NOT`                   | Checks if two values are not equal           |
| GREATER           | `>`, `GT`                     | Checks if the left value is greater           |
| GREATER_EQUAL     | `>=`, `GTE`                   | Checks if the left value is greater or equal |
| LESS              | `<`, `LT`                     | Checks if the left value is less             |
| LESS_EQUAL        | `<=`, `LTE`                   | Checks if the left value is less or equal    |

### Unary Operators

| Operator          | Symbols                       | Description                                  |
|-------------------|-------------------------------|----------------------------------------------|
| NULL              | `ISEMPTY`, `ISNULL`, `IS_EMPTY`, `IS_NULL` | Checks if a value is null                 |
| NOT_NULL          | `ISNOTEMPTY`, `ISNOTNULL`, `IS_NOT_EMPTY`, `IS_NOT_NULL` | Checks if a value is not null       |
| GREATER_ZERO      | `GTZ`, `GT0`                  | Checks if a value is greater than zero       |
| EQUAL_ZERO        | `EQZ`, `EQ0`                  | Checks if a value is equal to zero           |
| LESS_ZERO         | `LTZ`, `LT0`                  | Checks if a value is less than zero          |
| NOT_EQUAL_ZERO    | `NEZ`, `NE0`                  | Checks if a value is not equal to zero       |

## Syntax

Expressions are built using a combination of variables, constants, and operators. Here are the general rules:

- Variables and constants can be used in comparison operations.
- Logical operators (`AND`, `OR`) are used to combine multiple conditions.
- Groupings using parentheses `(` and `)` can be used to control the order of evaluation.

### Examples of Valid Expressions

1. `app=proxmox && type=bare-metal`
2. `app=kubernetes || type=vm`
3. `(app=proxmox && type=lxc) || ansible_host="10.100.4.100"`
4. `app!=proxmox`
5. `ansible_host="10.100.4.100"`
6. `type ISNULL`
7. `value GTZ`

## Examples

Here are some example expressions and their evaluations:

1. **Expression**: `app=proxmox && type=bare-metal`
   - **Description**: Checks if the `app` is `proxmox` and `type` is `bare-metal`.
   - **Evaluation**: True for `host1` with variables `{app: proxmox, type: bare-metal}`.

2. **Expression**: `(app=proxmox && type=lxc) || ansible_host="10.100.4.100"`
   - **Description**: Checks if the `app` is `proxmox` and `type` is `lxc`, or if `ansible_host` is `10.100.4.100`.
   - **Evaluation**: True for `host1` with `ansible_host: 10.100.4.100`.

3. **Expression**: `type ISNULL`
   - **Description**: Checks if the `type` is null.
   - **Evaluation**: True if `type` is not defined or is explicitly set to null.

4. **Expression**: `value GTZ`
   - **Description**: Checks if the `value` is greater than zero.
   - **Evaluation**: True if `value` is a positive number.

## Evaluation Process

The evaluation process follows these steps:

1. **Tokenization**: The expression is broken down into tokens.
2. **Shunting Yard Algorithm**: Converts the infix expression to a postfix expression (Reverse Polish Notation).
3. **Evaluation**: The postfix expression is evaluated using a stack-based approach.

### Tokenization

Tokenization is the process of breaking the expression into tokens. For example, the expression `app=proxmox && type=bare-metal` would be tokenized as:

1. `VARIABLE: app`
2. `COMPARISON_OPERATOR: =`
3. `CONSTANT: proxmox`
4. `LOGICAL_OPERATOR: &&`
5. `VARIABLE: type`
6. `COMPARISON_OPERATOR: =`
7. `CONSTANT: bare-metal`

### Shunting Yard Algorithm

This algorithm converts the infix expression into a postfix expression. For example, `app=proxmox && type=bare-metal` would be converted to:

1. `VARIABLE: app`
2. `CONSTANT: proxmox`
3. `COMPARISON_OPERATOR: =`
4. `VARIABLE: type`
5. `CONSTANT: bare-metal`
6. `COMPARISON_OPERATOR: =`
7. `LOGICAL_OPERATOR: &&`

### Evaluation

The postfix expression is evaluated using a stack-based approach. Each token is processed, and the stack is updated accordingly. For comparison and logical operators, the appropriate values are popped from the stack, the operation is performed, and the result is pushed back onto the stack.

## Debugging

### Global Debugging

To enable or disable debugging globally, use the `DEBUG_ENABLED` flag in the `global_debug_flags.py` file.

### Specific Debugging Flags

- `DEBUG_TOKENIZER`: Enable or disable debugging for the tokenizer.
- `DEBUG_EVALUATOR`: Enable or disable debugging for the evaluator.
- `DEBUG_EVALUATOR_CONDITIONS`: Specific debugging for condition evaluations.
- `DEBUG_EVALUATOR_SHUNTING_YARD`: Debugging for the shunting yard algorithm.

To use these flags, set them to `True` or `False` in the `global_debug_flags.py` file.

```python
# global_debug_flags.py

# If this is disabled, all debugging will be disabled
DEBUG_ENABLED = False

# Enable or disable debugging for tokenizer.
DEBUG_TOKENIZER = False

# Enable or disable debugging for expression evaluator.
DEBUG_EVALUATOR = True

# Specific debugging for conditions only.
DEBUG_EVALUATOR_CONDITIONS = True

# The shunting yard algorithm has its own specific debugging.
DEBUG_EVALUATOR_SHUNTING_YARD = False
```

## Conclusion

This document provides all the necessary information to build and evaluate expressions using the custom expression language. Use the provided examples and guidelines to create complex expressions tailored to your specific needs. If you encounter any issues, enable debugging to gain insights into the evaluation process.