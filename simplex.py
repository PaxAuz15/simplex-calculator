import sys
import numpy as np
from fractions import Fraction

try:
    import pandas as pd
    pandas_av = True
except ImportError:
    pandas_av = False
    pass

etiqueta_ecuaciones = []
col_values = []
ecuacionZ = []
filas_finales = []
soluciones = []
x = 'X'
ecuacionZ_2 = []
removable_vars = []
noHaySolucion = """
        ---Sin límites ----
Es posible que su problema no tenga solución debido a errores
formulación de restricciones,

Esto ocurre principalmente cuando omite algunas restricciones relevantes
por favor revise nuevamente la formulación de restricciones
            """


def main():
    global decimales
    global const_num, prod_nums
    print("""
    CALCULADORA - METODO SIMPLEX
    
    Qué tipo de problema quieres resolver?	
    1 :maximización (<=).
    2 :minimización (>=).
        
    0 :Para ayuda!
    """)
    try:
        prob_type = int(input("Ingrese el número del tipo de problema: >"))
    except ValueError:
        print("Ingrese un número de las opciones anteriores ")
        prob_type = int(input("Ingrese el número del tipo de problema: >"))
    if prob_type != 2 and prob_type != 1 and prob_type != 0:
        sys.exit("Usted escogió de manera incorrecta el tipo de problema ->" + str(prob_type))
    if prob_type == 0:
        print(r"""
        --HELP:
        CALCULADORA - METODO SIMPLEX
        
        ----- Requerimientos -----
        
        1 -> python - instalar python (https://www.python.org)
        2 -> pip    - instalar pip (google for your Operating System)
        3 -> numpy  - pip install numpy (comando unix)  - requerido!!
        4 -> pandas - pip install pandas (comando unix) - opcional - hace que el cuadro sea más hermoso y ordenado 
        
        ----- Elecciones -----
        
        1 -> Problemas de maximización simplex como maximización de ganancias 
        2 -> Problema de minimización simplex como minimización de gastos en empresa 
        0 -> Ayuda sobre el uso de la calculadora 
        
        ----- Ingrese mejores datos -----
        
        Renombre las variables segun los productos a analizar para X1, X2, X3...Xn
        para facilitar la alimentación de datos.
        
        n - siendo la cantidad de productos que tienes 
        
        ejemplo: computadoras - X1
                 impresoras   - X2

        Ud puede usar:  - números enteros
                        - n+umeros decimales
                        - fracciones
                Ingresando el valor que se le solicita. los decimales no se redondean al ingresar. 
                Esto asegura una alta precisión. para fracciones largas y recurrentes, 
                es decir. (1/3). los lugares decimales están ajustados al valor predeterminado de Python 
         
        Se recomienda utilizar valores inferiores a 10000000(diez millones). 
        Puede estandarizar los datos dividiéndolos en valores pequeños 
        y volviendo a convertirlos después de obtener la solución. 
         
        Los valores grandes se utilizan para la holgura en este programa. 
        Por lo que el uso de valores grandes puede generar confusión 
        de datos con las variables de holgura en algunos casos 
          
        
        ----- Supuestos -----
        
        Supongo que sabes leer la tabla simplex. 
        También asumo que sabes cómo interpretar los datos en la tabla y 
        por eso no interpreté los datos 
        
        Este programa debe ser utilizado por estadísticos y 
        también por aquellos que tengan una idea sobre los problemas simplex. 
        
        Sin embargo, estos programas no necesitan mucho conocimiento en matemáticas / estadística 
        
        ----- Problemas de método simplex mixtos -----
          
        No he hecho una elección para el problema de símplex mixto y, 
        por ahora, es posible que el programa no proporcione una 
        solución para tales problemas. 
         
        ----- OJO -----
        
        Solo la opción de consola de este programa está disponible todavía, 
        pero la GUI podría estar disponible en algún momento y, cuando esté disponible, 
        actualizaré sobre cómo usar la GUI. 
          
        #Puede sugerir adiciones o incluso enviarme errores en el programa en el correo electrónico a continuación .#
          
        luisauzm07ci@gmail.com
        
        
           
        ----- licencia -----
        
        Este programa debe utilizarse libremente. También puede volver a 
        editar o modificar o incluso agregar a este programa.
        También puede compartir, pero no debe cambiar la propiedad del desarrollador. 
        
        Agradeceré el crédito que se me haya dado 
        
        ----- desarrollador -----
          
        desarrollado por [LUIS AUZ GARCIA] .
        Estudiante de Investigación de Operaciones.
        ULEAM, Ecuador.
        Email   : luisauzm07ci@gmail.com         
        
         
        """)
        sys.exit()
    print('\n##########################################')
    global const_names
    const_num = int(input("Cuántos productos tienes?: >"))
    prod_nums = int(input("Cuántas condiciones tienes?: >"))
    const_names = [x + str(i) for i in range(1, const_num + 1)]
    for i in range(1, prod_nums + 1):
        prod_val = input("Ingrese el nombre de la condición {}: >".format(i))
        etiqueta_ecuaciones.append(prod_val)
    print("__________________________________________________")
    if prob_type == 1:
        for i in const_names:
            try:
                val = float(Fraction(input("ingrese el valor de  %s en la ecuación Z: >" % i)))
            except ValueError:
                print("Por favor, Ingrese solo valores numéricos")
                val = float(Fraction(input("Ingrese el valor de  %s en la ecuación Z: >" % i)))
            ecuacionZ.append(0 - int(val))
        ecuacionZ.append(0)

        while len(ecuacionZ) <= (const_num + prod_nums):
            ecuacionZ.append(0)
        print("__________________________________________________")
        for prod in etiqueta_ecuaciones:
            for const in const_names:
                try:
                    val = float(Fraction(input("Ingrese el valor de %s en %s: >" % (const, prod))))
                except ValueError:
                    print("Por favor, ingrese solo valores numéricos")
                    val = float(Fraction(input("Ingrese el valor de %s en %s: >" % (const, prod))))
                col_values.append(val)
            equate_prod = float(Fraction(input('Igualar %s a: >' % prod)))
            col_values.append(equate_prod)

        final_cols = stdz_rows(col_values)
        i = len(const_names) + 1
        while len(const_names) < len(final_cols[0]) - 1:
            const_names.append('X' + str(i))
            soluciones.append('X' + str(i))
            i += 1
        soluciones.append(' Z')
        const_names.append('Solución')
        final_cols.append(ecuacionZ)
        filas_finales = np.array(final_cols).T.tolist()
        print("_____________________________________________")
        decimales = int(input('Número de decimales para redondear : '))
        print('\n##########################################')
        maximization(final_cols, filas_finales)

    elif prob_type == 2:
        for i in const_names:
            try:
                val = float(Fraction(input("Ingrese el valor de %s en la ecuación Z: >" % i)))
            except ValueError:
                print("Por favor, Ingrese un número")
                val = float(Fraction(input("Ingrese el valor de %s en la ecuación Z: >" % i)))
            ecuacionZ.append(val)
        ecuacionZ.append(0)

        while len(ecuacionZ) <= (const_num + prod_nums):
            ecuacionZ.append(0)
        print("__________________________________________________")
        for prod in etiqueta_ecuaciones:
            for const in const_names:
                try:
                    val = float(Fraction(input("Ingrese el valor de %s en %s: >" % (const, prod))))
                except ValueError:
                    print("Por favor, Ingrese un número")
                    val = float(Fraction(input("Ingrese el valor de %s en %s: >" % (const, prod))))
                col_values.append(val)
            equate_prod = float(Fraction(input('Igualar %s a: >' % prod)))
            col_values.append(equate_prod)

        final_cols = stdz_rows2(col_values)
        i = len(const_names) + 1
        while len(const_names) < prod_nums + const_num:
            const_names.append('X' + str(i))
            soluciones.append('X' + str(i))
            i += 1
        soluciones.append(' Z')
        soluciones[:] = []
        add_from = len(const_names) + 1
        while len(const_names) < len(final_cols[0][:-1]):
            removable_vars.append('X' + str(add_from))
            const_names.append('X' + str(add_from))
            add_from += 1
        removable_vars.append(' Z')
        removable_vars.append('Z1')
        const_names.append('Solución')
        for ems in removable_vars:
            soluciones.append(ems)
        while len(ecuacionZ) < len(final_cols[0]):
            ecuacionZ.append(0)
        final_cols.append(ecuacionZ)
        final_cols.append(ecuacionZ_2)
        filas_finales = np.array(final_cols).T.tolist()
        print("________________________________")
        decimales = int(input('Número de decimales para redondear : '))
        print('\n##########################################')
        minimization(final_cols, filas_finales)

    else:
        sys.exit("Ud ingresó una opción de problema incorrecta->" + str(prob_type))


def maximization(final_cols, filas_finales):
    row_app = []
    last_col = final_cols[-1]
    min_last_row = min(last_col)
    min_manager = 1
    print(" 1 TABLA")
    try:
        final_pd = pd.DataFrame(np.array(final_cols), columns=const_names, index=soluciones)
        print(final_pd)
    except:
        print('  ', const_names)
        i = 0
        for cols in final_cols:
            print(soluciones[i], cols)
            i += 1
    count = 2
    pivot_element = 2
    while min_last_row < 0 < pivot_element != 1 and min_manager == 1 and count < 6:
        print("*********************************************************")
        last_col = final_cols[-1]
        last_row = filas_finales[-1]
        min_last_row = min(last_col)
        index_of_min = last_col.index(min_last_row)
        pivot_row = filas_finales[index_of_min]
        index_pivot_row = filas_finales.index(pivot_row)
        row_div_val = []
        i = 0
        for _ in last_row[:-1]:
            try:
                val = float(last_row[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        pivot_col = final_cols[index_min_div_val]
        index_pivot_col = final_cols.index(pivot_col)
        row_app[:] = []
        for col in final_cols:
            if col is not pivot_col and col is not final_cols[-1]:
                form = col[index_of_min] / pivot_element
                final_val = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) - final_val), decimales)).tolist()
                final_cols[final_cols.index(col)] = new_col

            elif col is pivot_col:
                new_col = (np.round((np.array(col) / pivot_element), decimales)).tolist()
                final_cols[final_cols.index(col)] = new_col
            else:
                form = abs(col[index_of_min]) / pivot_element
                final_val = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) + final_val), decimales)).tolist()
                final_cols[final_cols.index(col)] = new_col
        filas_finales[:] = []
        re_filas_finales = np.array(final_cols).T.tolist()
        filas_finales = filas_finales + re_filas_finales

        if min(row_div_val) != 10000000000:
            min_manager = 1
        else:
            min_manager = 0
        print('elemento pivote: %s' % pivot_element)
        print('columna pivote: ', pivot_row)
        print('fila pivote: ', pivot_col)
        print("\n")
        soluciones[index_pivot_col] = const_names[index_pivot_row]

        print(" %d TABLA" % count)
        try:
            final_pd = pd.DataFrame(np.array(final_cols), columns=const_names, index=soluciones)
            print(final_pd)
        except:
            print("%d TABLA" % count)
            print('  ', const_names)
            i = 0
            for cols in final_cols:
                print(soluciones[i], cols)
                i += 1
        count += 1
        last_col = final_cols[-1]
        last_row = filas_finales[-1]
        min_last_row = min(last_col)
        index_of_min = last_col.index(min_last_row)
        pivot_row = filas_finales[index_of_min]
        row_div_val = []
        i = 0
        for _ in last_row[:-1]:
            try:
                val = float(last_row[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        if pivot_element < 0:
            print(noHaySolucion)
    if not pandas_av:
        print("""
        Instale pandas para que sus tablas se vean bien 
        instale usando el comando $ pip install pandas 
        """)


def minimization(final_cols, filas_finales):
    row_app = []
    last_col = final_cols[-1]
    min_last_row = min(last_col)
    min_manager = 1
    print("1 TABLA")
    try:
        fibal_pd = pd.DataFrame(np.array(final_cols), columns=const_names, index=soluciones)
        print(fibal_pd)
    except:
        print('  ', const_names)
        i = 0
        for cols in final_cols:
            print(soluciones[i], cols)
            i += 1
    count = 2
    pivot_element = 2
    while min_last_row < 0 < pivot_element and min_manager == 1:
        print("*********************************************************")
        last_col = final_cols[-1]
        last_row = filas_finales[-1]
        min_last_row = min(last_col[:-1])
        index_of_min = last_col.index(min_last_row)
        pivot_row = filas_finales[index_of_min]
        index_pivot_row = filas_finales.index(pivot_row)
        row_div_val = []
        i = 0
        for _ in last_row[:-2]:
            try:
                val = float(last_row[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        pivot_col = final_cols[index_min_div_val]
        index_pivot_col = final_cols.index(pivot_col)
        row_app[:] = []
        for col in final_cols:
            if col is not pivot_col and col is not final_cols[-1]:
                form = col[index_of_min] / pivot_element
                final_form = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) - final_form), decimales)).tolist()
                final_cols[final_cols.index(col)] = new_col
            elif col is pivot_col:
                new_col = (np.round((np.array(col) / pivot_element), decimales)).tolist()
                final_cols[final_cols.index(col)] = new_col
            else:
                form = abs(col[index_of_min]) / pivot_element
                final_form = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) + final_form), decimales)).tolist()
                final_cols[final_cols.index(col)] = new_col
        filas_finales[:] = []
        re_filas_finales = np.array(final_cols).T.tolist()
        filas_finales = filas_finales + re_filas_finales
        if min(row_div_val) != 10000000000:
            min_manager = 1
        else:
            min_manager = 0
        print('elemento pivote: %s' % pivot_element)
        print('columna pivote: ', pivot_row)
        print('fila pivote: ', pivot_col)
        print("\n")
        removable = soluciones[index_pivot_col]
        soluciones[index_pivot_col] = const_names[index_pivot_row]
        if removable in removable_vars:
            idex_remove = const_names.index(removable)
            for colms in final_cols:
                colms.remove(colms[idex_remove])
            const_names.remove(removable)
        print("%d TABLA" % count)
        try:
            fibal_pd = pd.DataFrame(np.array(final_cols), columns=const_names, index=soluciones)
            print(fibal_pd)
        except:
            print('  ', const_names)
            i = 0
            for cols in final_cols:
                print(soluciones[i], cols)
                i += 1
        count += 1
        filas_finales[:] = []
        new_filas_finales = np.array(final_cols).T.tolist()
        for _list in new_filas_finales:
            filas_finales.append(_list)

        last_col = final_cols[-1]
        last_row = filas_finales[-1]
        min_last_row = min(last_col[:-1])
        index_of_min = last_col.index(min_last_row)
        pivot_row = filas_finales[index_of_min]
        row_div_val = []
        i = 0
        for _ in last_row[:-2]:
            try:
                val = float(last_row[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        if pivot_element < 0:
            print(noHaySolucion)

    if not pandas_av:
        print("""
        Instale pandas para que sus tablas se vean bien 
        instale usando el comando $ pip install pandas 
        """)


def stdz_rows2(column_values):
    final_cols = [column_values[x:x + const_num + 1] for x in range(0, len(column_values), const_num + 1)]
    sum_z = (0 - np.array(final_cols).sum(axis=0)).tolist()
    for _list in sum_z:
        ecuacionZ_2.append(_list)

    for cols in final_cols:
        while len(cols) < (const_num + (2 * prod_nums) - 1):
            cols.insert(-1, 0)

    i = const_num
    for sub_col in final_cols:
        sub_col.insert(i, -1)
        ecuacionZ_2.insert(-1, 1)
        i += 1

    for sub_col in final_cols:
        sub_col.insert(i, 1)
        i += 1

    while len(ecuacionZ_2) < len(final_cols[0]):
        ecuacionZ_2.insert(-1, 0)

    return final_cols


def stdz_rows(column_values):
    final_cols = [column_values[x:x + const_num + 1] for x in range(0, len(column_values), const_num + 1)]
    for cols in final_cols:
        while len(cols) < (const_num + prod_nums):
            cols.insert(-1, 0)

    i = const_num
    for sub_col in final_cols:
        sub_col.insert(i, 1)
        i += 1

    return final_cols


if __name__ == "__main__":
    main()

# Utilizo listas y matrices de Python (numpy) en la mayor parte de este programa
# se volvió simple porque python tiene un gran poder en la manipulación y solución de listas y matrices 
