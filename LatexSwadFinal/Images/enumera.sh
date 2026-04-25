#!/bin/bash

directorio=1  # 0=activar directorios, 1=desactivar
archivo=0     # 0=activar archivos, 1=desactivar  
ind=1         # 1=índices desactivados, 0=activados
nom=1         # 1=eliminar nombre original, 0=mantener
dir=""
arch=""
i=1
expr_reg=""
base=""
exts=""
modo_find=0

while getopts "he:iI:b:dD:oA::x:np" opt; do  # ← Añadida 'p'
    case $opt in
        d) directorio=0 ;;
        D) dir="$OPTARG" ;;
        b) base="$OPTARG" ;;
        i) ind=0 ;;
        I) i=$OPTARG ;;
        e) expr_reg="$OPTARG" ;;
        o) archivo=1 ;;
        A) arch="$OPTARG" ;;
        x) exts="$OPTARG" ;;
        n) nom=0 ;;
        p) modo_find=1 ;;  # ← NUEVA opción para patrones con espacios
        h) 
            echo -e "Uso: ./enumera.sh [OPTIONS] [ARGS]"
            echo -e "\nOpciones:"
            echo -e "  -h: este mensaje"
            echo -e "  -e: expresión regular (entre comillas: 'a*.txt')"
            echo -e "  -i: activar índices numéricos"
            echo -e "  -I: índice inicial (ej: -I 10)"
            echo -e "  -d: procesar directorios"
            echo -e "  -D: prefijo para directorios (ej: -D 'dir_')"
            echo -e "  -o: desactivar archivos"
            echo -e "  -A: prefijo para archivos (ej: -A 'file_')"
            echo -e "  -x: cambiar extensiones (ej: -x 'txt:jpg,png:pdf')"
            echo -e "  -n: mantener nombre original"
            echo -e "  -p: usar find para patrones con espacios (ej: '* *.tct')"
            echo -e "\nEjemplo: ./enumera.sh -e 'a*.txt' -i -I 1 -A 'b' -n"
            echo -e "         ./enumera.sh -e '* *.tct' -i -I 1 -A 'b' -p"
            exit 0
            ;;
        *) echo "Opción inválida. Usa -h para ayuda."; exit 1 ;;
    esac
done

shift $((OPTIND-1))

# Configuraciones por defecto
if [[ -z "$base" ]]; then base=""; fi
if [[ -z "$expr_reg" ]]; then expr_reg="$*"; fi
if [[ ! "$i" =~ ^[0-9]+$ ]]; then i=1; fi

# Procesar sustituciones de extensiones
declare -A exts_map
if [[ -n "$exts" ]]; then
    IFS=',' read -ra pares <<< "$exts"
    for par in "${pares[@]}"; do
        clave="${par%%:*}"
        valor="${par#*:}"
        [[ -n "$clave" ]] && exts_map["$clave"]="$valor"
    done
fi

# Bucle principal - Opción 3: detectar espacios automáticamente
if [[ "$modo_find" == 1 ]]; then
    # MODO FIND para patrones con espacios
    echo "🔍 Buscando con patrón: $expr_reg"
    while IFS= read -r -d '' _archivo; do
        _archivo="${_archivo#./}"  # Quitar prefijo ./ si lo tiene
        
        [[ ! -e "$_archivo" ]] && continue
        
        _i=""
        [[ "$ind" == 0 ]] && _i="$i"
        
        if [[ -f "$_archivo" && "$archivo" == 0 ]]; then
            # Procesar ARCHIVO
            nombre_base="${_archivo%.*}"
            extension="${_archivo##*.}"
            [[ "$extension" == "$_archivo" ]] && extension=""
            
            [[ "$nom" == 1 ]] && nombre_base=""
            
            nueva_ext="$extension"
            [[ -n "${exts_map[$extension]}" ]] && nueva_ext="${exts_map[$extension]}"
            
            nuevo_nombre="${arch}${base}${_i}${nombre_base}"
            [[ -n "$nueva_ext" ]] && nuevo_nombre+=".${nueva_ext}"
            
            mv -v "$_archivo" "$nuevo_nombre"
            
        elif [[ -d "$_archivo" && "$directorio" == 0 ]]; then
            # Procesar DIRECTORIO
            dir_nom="${_archivo##*/}"
            [[ "$nom" == 1 ]] && dir_nom=""
            
            nuevo_dir="${dir}${base}${_i}${dir_nom}"
            mv -v "$_archivo" "$nuevo_dir"
        fi
        
        i=$((i + 1))
    done < <(find . -maxdepth 1 -name "$expr_reg" -print0 2>/dev/null)
    
else
    # MODO NORMAL (tu código original)
    for _archivo in $expr_reg; do
        [[ ! -e "$_archivo" ]] && continue
        
        _i=""
        [[ "$ind" == 0 ]] && _i="$i"
        
        if [[ -f "$_archivo" && "$archivo" == 0 ]]; then
            nombre_base="${_archivo%.*}"
            extension="${_archivo##*.}"
            [[ "$extension" == "$_archivo" ]] && extension=""
            
            [[ "$nom" == 1 ]] && nombre_base=""
            
            nueva_ext="$extension"
            [[ -n "${exts_map[$extension]}" ]] && nueva_ext="${exts_map[$extension]}"
            
            nuevo_nombre="${arch}${base}${_i}${nombre_base}"
            [[ -n "$nueva_ext" ]] && nuevo_nombre+=".${nueva_ext}"
            
            mv -v "$_archivo" "$nuevo_nombre"
            
        elif [[ -d "$_archivo" && "$directorio" == 0 ]]; then
            dir_nom="${_archivo##*/}"
            [[ "$nom" == 1 ]] && dir_nom=""
            
            nuevo_dir="${dir}${base}${_i}${dir_nom}"
            mv -v "$_archivo" "$nuevo_dir"
        fi
        
        i=$((i + 1))
    done
fi