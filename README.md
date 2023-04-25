# bank-account-statement-parser
A simple program to transfer your bank statements into an excel file. The programme can recognise and assign simple keywords in the transactions and offers a simple GUI to select the pdfs and excel file. 


# Install
### Directory Structure
Not much needs to be taken care of, only that if a default path for the Excel is chosen (see Using), a configuration folder and file will be created in the same folder as the program. To use the config the program needs to be in the same folder, something like this:
```bash
bank-account-statement-parser
├───config_parser
│   └───config.json
├───Bank-Account-Statement-Parser-1.0.0.exe
```
This is also valid if you are using the plain python files.

### Using the exe
If you are usiong the exe you should be ready to go without any installations except python itself.

### If you are not using the exe
Frist you need to install some packages to run the python file. For that we provide a requirements.txt. We assume you have allready installed python and pip.
```bash
pip install -r requirements.txt
```
After the successful installation yqu are ready to go. To execute the program just double click on the GUI_pathfinder.py or use the command line with the command:
```bash
python GUI_pathfinder.py
```


