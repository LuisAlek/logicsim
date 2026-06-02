### CORTE 1 Y 2: Código base (ya entregado)
### CORTE 3: Análisis Interactivo de Secuencias y Métricas con Series

import re
import itertools
import argparse
import sys

# ─────────────────────────────────────────────
#  CORTE 1 Y 2: Funciones base (sin modificar)
# ─────────────────────────────────────────────

def parse_expression(expression_str):
    """Parser expandido: ~ (NOT), & (AND), | (OR), -> (IF), <-> (IFF)"""
    precedencia = {'~': 4, '&': 3, '|': 2, '->': 1, '<->': 1}
    salida = []
    pila = []
    tokens = re.findall(r'[a-zA-Z0-9]+|<->|->|[~&|()]', expression_str)

    for token in tokens:
        if token.isalnum():
            salida.append(token)
        elif token == '(':
            pila.append(token)
        elif token == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()
        else:
            while (pila and pila[-1] != '(' and
                   precedencia.get(token, 0) <= precedencia.get(pila[-1], 0)):
                salida.append(pila.pop())
            pila.append(token)
    while pila:
        salida.append(pila.pop())
    return salida


def get_variables(expression_str):
    """Obtiene variables únicas usando la estructura 'set'."""
    tokens = re.findall(r'[a-zA-Z0-9]+', expression_str)
    return sorted(list(set(tokens)))


def evaluate_expression(parsed_expression, variable_values):
    """Motor de evaluación."""
    pila = []
    for token in parsed_expression:
        if token.isalnum():
            pila.append(variable_values[token])
        elif token == '~':
            pila.append(not pila.pop())
        else:
            v2 = pila.pop()
            v1 = pila.pop()
            if token == '&':    pila.append(v1 and v2)
            elif token == '|':  pila.append(v1 or v2)
            elif token == '->': pila.append(not v1 or v2)
            elif token == '<->': pila.append(v1 == v2)
    return pila[0]


def get_minterms(expression_str, variables_unificadas=None):
    """Calcula el conjunto de minitérminos (combinaciones que dan True)."""
    variables = variables_unificadas if variables_unificadas else get_variables(expression_str)
    parsed_expr = parse_expression(expression_str)
    minterminos = set()
    combinaciones = list(itertools.product([True, False], repeat=len(variables)))
    for comb in combinaciones:
        valores = dict(zip(variables, comb))
        if evaluate_expression(parsed_expr, valores):
            minterminos.add(comb)
    return minterminos


def generate_truth_table(expression_str):
    """Imprime la tabla de verdad completa."""
    variables = get_variables(expression_str)
    parsed_expr = parse_expression(expression_str)
    header = " | ".join(variables) + " | RESULTADO"
    print(f"\nTabla de verdad para: {expression_str}")
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    combinaciones = list(itertools.product([True, False], repeat=len(variables)))
    for comb in combinaciones:
        valores = dict(zip(variables, comb))
        res = evaluate_expression(parsed_expr, valores)
        fila = " | ".join(["V" if v else "F" for v in comb])
        print(f"{fila} | {'V' if res else 'F'}")


def are_equivalent(expr1, expr2):
    """Determina si dos expresiones son equivalentes basándose en minitérminos."""
    vars_all = sorted(list(set(get_variables(expr1) + get_variables(expr2))))
    m1 = get_minterms(expr1, vars_all)
    m2 = get_minterms(expr2, vars_all)
    print(f"\nComparando equivalencia:")
    print(f"E1: {expr1}")
    print(f"E2: {expr2}")
    if m1 == m2:
        print("\n[RESULTADO]: Las expresiones son LÓGICAMENTE EQUIVALENTES.")
        return True
    else:
        print("\n[RESULTADO]: Las expresiones NO son equivalentes.")
        return False


# ─────────────────────────────────────────────
#  CORTE 3: Series, costos y simulación interactiva
# ─────────────────────────────────────────────

# Costo definido para cada tipo de compuerta (Serie Estática)
GATE_COSTS = {
    '~':   1,   # NOT
    '&':   2,   # AND
    '|':   2,   # OR
    '->':  3,   # Condicional
    '<->': 4    # Bicondicional
}


def calculate_construction_cost(expression_str):
    """
    SERIE ESTÁTICA: Calcula el costo de construcción del circuito.
    Recorre los tokens de la expresión y suma el costo de cada compuerta.
    Fórmula: Costo_Total = Σ costo(compuerta_i)
    Retorna: (costo_total, lista_de_compuertas)
    """
    tokens = re.findall(r'[a-zA-Z0-9]+|<->|->|[~&|()]', expression_str)
    compuertas_encontradas = []
    for token in tokens:
        if token in GATE_COSTS:
            compuertas_encontradas.append(token)
    costo_total = sum(GATE_COSTS[g] for g in compuertas_encontradas)
    return costo_total, compuertas_encontradas


def evaluate_with_cost_tracking(parsed_expression, variable_values):
    """
    SERIE DINÁMICA: Evalúa la expresión y registra qué compuertas
    se activaron (produjeron True) en este paso.
    Retorna: (resultado_final, lista_compuertas_activadas)
    """
    pila_valores = []
    pila_gates  = []

    for token in parsed_expression:
        if token.isalnum():
            pila_valores.append(variable_values[token])
            pila_gates.append([])
        elif token == '~':
            val   = pila_valores.pop()
            gates = pila_gates.pop()
            resultado = not val
            gates_activadas = gates + (['~'] if resultado else [])
            pila_valores.append(resultado)
            pila_gates.append(gates_activadas)
        else:
            v2 = pila_valores.pop()
            v1 = pila_valores.pop()
            g2 = pila_gates.pop()
            g1 = pila_gates.pop()

            if token == '&':    resultado = v1 and v2
            elif token == '|':  resultado = v1 or v2
            elif token == '->': resultado = not v1 or v2
            elif token == '<->': resultado = v1 == v2
            else: resultado = False

            gates_activadas = g1 + g2 + ([token] if resultado else [])
            pila_valores.append(resultado)
            pila_gates.append(gates_activadas)

    return pila_valores[0], pila_gates[0]


def calculate_operation_cost(activated_gates):
    """
    Calcula el costo de operación de UN paso (Serie Dinámica).
    Suma solo las compuertas que se activaron (resultado True).
    """
    return sum(GATE_COSTS.get(g, 0) for g in activated_gates)


def parse_variable_input(user_input):
    """
    Parsea una línea como 'P=V,Q=F' y retorna {'P': True, 'Q': False}.
    Acepta V/v/1 como verdadero y F/f/0 como falso.
    """
    variable_values = {}
    parts = user_input.replace(' ', '').split(',')
    for part in parts:
        if '=' not in part:
            raise ValueError(f"Formato incorrecto en '{part}'. Usa VAR=V o VAR=F")
        var, val = part.split('=', 1)
        val = val.strip().upper()
        if val in ('V', '1', 'TRUE'):
            variable_values[var.strip()] = True
        elif val in ('F', '0', 'FALSE'):
            variable_values[var.strip()] = False
        else:
            raise ValueError(f"Valor inválido '{val}'. Usa V o F")
    return variable_values


def interactive_simulation_mode(expression_str):
    """
    CORTE 3 - Modo de Simulación Interactiva de Secuencias.

    Aplica:
    - Serie Estática : costo de construcción (se calcula una sola vez).
    - Serie Dinámica : costo de operación por cada paso de la sucesión.
    - Sumatoria final: Σ costos_por_paso al terminar la secuencia.
    """
    print("=" * 56)
    print("   LOGICSIM - ANÁLISIS DE SECUENCIA INTERACTIVA (CORTE 3)")
    print("=" * 56)
    print(f"Expresión: {expression_str}\n")

    # Parsear la expresión una sola vez
    try:
        parsed_expr = parse_expression(expression_str)
    except Exception as e:
        print(f"[ERROR] Expresión inválida: {e}")
        return

    # ── [1] COSTO DE CONSTRUCCIÓN (Serie Estática) ──────────────────
    costo_construccion, compuertas = calculate_construction_cost(expression_str)
    print(f"[1] Costo de Construcción del Circuito: {costo_construccion}")
    print(f"    Compuertas detectadas : {compuertas}")
    detalle = ' + '.join(str(GATE_COSTS[g]) for g in compuertas)
    print(f"    Detalle               : {detalle} = {costo_construccion}")

    # ── [2] BUCLE INTERACTIVO DE SECUENCIAS ─────────────────────────
    variables_esperadas = get_variables(expression_str)
    print(f"\n[2] Ingrese la Sucesión de Entradas")
    print(f"    Variables requeridas : {variables_esperadas}")
    print(f"    Formato              : {','.join(v + '=V' for v in variables_esperadas)}")
    print("    (Presione Enter en una línea vacía para finalizar)\n")

    total_pasos          = 0
    costo_operacion_total = 0
    historial            = []   # (paso, entradas, salida, costo_paso)

    while True:
        try:
            entrada = input(f"t={total_pasos + 1}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not entrada:
            break

        # Parsear entradas del usuario
        try:
            valores_variables = parse_variable_input(entrada)
        except ValueError as e:
            print(f"    [!] Error: {e}")
            print(f"    Ejemplo: {','.join(v + '=V' for v in variables_esperadas)}")
            continue

        # Verificar que estén todas las variables
        faltantes = set(variables_esperadas) - set(valores_variables.keys())
        if faltantes:
            print(f"    [!] Faltan variables: {', '.join(sorted(faltantes))}")
            continue

        # Evaluar con seguimiento de compuertas activadas
        try:
            resultado, compuertas_activadas = evaluate_with_cost_tracking(
                parsed_expr, valores_variables
            )
        except Exception as e:
            print(f"    [!] Error en evaluación: {e}")
            continue

        # Costo de operación de este paso
        costo_paso             = calculate_operation_cost(compuertas_activadas)
        costo_operacion_total += costo_paso   # Σ costos_por_paso
        total_pasos           += 1

        historial.append((total_pasos, valores_variables.copy(), resultado, costo_paso))

        # Resultado inmediato
        activadas_str = compuertas_activadas if compuertas_activadas else ['ninguna']
        print(f"-> Salida: {'V' if resultado else 'F'} | "
              f"Costo Op.: {costo_paso} | "
              f"Activadas: {activadas_str}")

    # ── REPORTE FINAL ────────────────────────────────────────────────
    print("\n" + "-" * 56)
    print("                   REPORTE FINAL")
    print("-" * 56)
    print(f"- Expresión Analizada             : {expression_str}")
    print(f"- Compuertas del Circuito         : {compuertas}")
    print(f"- Costo de Construcción           : {costo_construccion}")
    print(f"- Pasos de la Secuencia Simulados : {total_pasos}")
    print(f"- Costo Total de Operación")
    print(f"  Acumulado (Σ costos_por_paso)   : {costo_operacion_total}")

    if historial:
        print()
        print(f"  {'Paso':<6} {'Entradas':<28} {'Salida':<8} {'Costo Op.'}")
        print(f"  {'----':<6} {'-------':<28} {'------':<8} {'---------'}")
        for paso, asignacion, res, costo in historial:
            entradas_str = ", ".join(
                f"{k}={'V' if v else 'F'}" for k, v in sorted(asignacion.items())
            )
            print(f"  {paso:<6} {entradas_str:<28} {'V' if res else 'F':<8} {costo}")

    print("-" * 56)


# ─────────────────────────────────────────────
#  MAIN: Interfaz de línea de comandos
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LogicSim - Simulador de Circuitos Lógicos UCMC",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Flags del Corte 2 (ya existentes)
    parser.add_argument(
        "--tabla-verdad",
        type=str,
        metavar="EXPR",
        help="Imprime la tabla de verdad\n  Ej: --tabla-verdad \"P -> Q\""
    )
    parser.add_argument(
        "--comparar",
        nargs=2,
        metavar=("EXPR1", "EXPR2"),
        help="Compara si dos expresiones son equivalentes\n  Ej: --comparar \"~(A&B)\" \"~A|~B\""
    )

    # Flag nuevo del Corte 3
    parser.add_argument(
        "-si", "--secuencia-interactiva",
        type=str,
        metavar="EXPR",
        dest="secuencia_interactiva",
        help=(
            "Modo simulación interactiva de secuencias (Corte 3)\n"
            "  Ej: -si \"(P | ~Q) & P\"\n"
            "  Costos: ~=1  &=2  |=2  ->=3  <->=4"
        )
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.tabla_verdad:
        generate_truth_table(args.tabla_verdad)

    elif args.comparar:
        are_equivalent(args.comparar[0], args.comparar[1])

    elif args.secuencia_interactiva:
        interactive_simulation_mode(args.secuencia_interactiva)


if __name__ == "__main__":
    main()
