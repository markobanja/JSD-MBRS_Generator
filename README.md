
Marko Purić - R2 38/2021
# JSD-MBRS Generator

* DSL language created with **TextX**.
* GUI created with **Python** and **tkinter**.
# Main idea
<div style="display: flex; justify-content: space-between;">
    <img src="readme_assets/python.png" width="150" height="150">
    <img src="readme_assets/textX.png" width="200" height="100" style="align-self: center;">
    <img src="readme_assets/jinja.png">
</div>

Main idea for this project is to create domain specific language with TextX and Python which will speed up the process of creating and generating code (classes - more specific under [**Functionalities**](#Functionalities)).
User just need to learn syntax (help window will be created inside GUI). Syntax is more human oriented and it will make life easier for developers.

DSL will recognize classes for:
  - Python
  - C#
  - Java

Jinja2 will be used as a template  which will generate codes (classes) for mentioned programming languages.
## What you get with this DSL:
* Automatization
* Time efficiency in coding and deployment
* Less coding syntax errors
* Standardization and consistency
## Visualisation:
* .dot (meta model and model)
* PlantUML (meta model)
# Functionalities:
### With this DSL you will be able to create:
* **Parameters** (for every parameter you will be able to generate get/set methods).

  For every parameters you will be able to generate different **data types** (basic and advanced). For all advanced data types DSL will be able to recognize **imports** too.
* **Constants**
* **Constructors**:
  - Default - where you have all declared parameters.
  - Empty
  - Specific parameters
* **Functions**:
  - Void 
  - Return
      
Logic of the functions should be written manually. It will be prohibited to have same constructors, parameters or functions.
