#!/bin/bash

# Asegurar el uso de la instalación funcional de TeX Live 2024 si existe
if [ -d "/usr/local/texlive/2024/bin/x86_64-linux" ]; then
    export PATH="/usr/local/texlive/2024/bin/x86_64-linux:$PATH"
fi

archivo="main"
borrar_logs=0
interactivo=nonstopmode
while getopts "hrsm:" opt; do
    case $opt in
        r) borrar_logs=1 ;;
        m) archivo="$OPTARG" ;;
        s) interactivo=batchmode ;;
        h) 
            echo -e "Uso: ./pdf.sh [OPTIONS] [ARGS]"
            echo -e "\nOpciones:"
            echo -e "  -h: este mensaje"
            echo -e "  -m: clear pdf a partir de un archivo .tex distinto de 'main'"
            echo -e "  -r: borrar logs"
            echo -e "  -s: modo silencioso"
            echo -e "./pdf.sh -s -r  # para no producir logs, borrarlos y no imprimir por pantalla"
            exit 0
            ;;
        *) echo "Opción inválida. Usa -h para ayuda."; exit 1 ;;
    esac
done

if [[ "$borrar_logs" -eq "1" ]]; then
    xelatex  -synctex=1 -interaction=$interactivo -file-line-error  "./$archivo.tex"
    biber $archivo
    xelatex  -synctex=1 -interaction=$interactivo -file-line-error  "./$archivo.tex"
    xelatex  -synctex=1 -interaction=$interactivo -file-line-error  "./$archivo.tex"

    ls | grep -P "$archivo\.(?!(pdf|tex)$)" | xargs rm #-v
else
    xelatex  -synctex=1 -interaction=$interactivo -file-line-error -recorder  "./$archivo.tex"
    biber $archivo
    xelatex  -synctex=1 -interaction=$interactivo -file-line-error  "./$archivo.tex"
    xelatex  -synctex=1 -interaction=$interactivo -file-line-error  "./$archivo.tex"

fi
