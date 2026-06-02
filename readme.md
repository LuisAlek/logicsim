# LogicSim - Simulador de Circuitos Lógicos UCMC (Corte 3)

**Institución:** Universidad Colegio Mayor del Cauca  
**Facultad:** Facultad de Ingeniería  
**Programa:** Tecnología en Desarrollo de Software / Sistemas  
**Asignatura:** Estructuras Discretas / Lógica Computacional  

---

## 📝 Descripción del Proyecto

**LogicSim** es una herramienta educativa e interactiva desarrollada en Python orientada al modelado, análisis y evaluación de expresiones de lógica proposicional. El sistema traduce fórmulas lógicas tradicionales a estructuras de circuitos equivalentes para calcular su comportamiento booleano.

Para este **Corte 3**, el simulador incorpora un robusto **Análisis Interactivo de Secuencias y Métricas de Series**, permitiendo la simulación de señales temporales discretas ($t$) sobre un circuito virtual. Esto facilita el estudio de la eficiencia de una expresión lógica mediante la cuantificación del costo físico y operativo de las compuertas que la componen.

---

## 🛠️ Nuevas Funcionalidades (Corte 3)

El software clasifica y calcula el consumo de recursos de los circuitos lógicos basándose en dos tipos de series matemáticas:

### 1. Sistema de Pesos por Compuerta
Cada operador lógico implementado posee un costo energético/físico de hardware predefinido de acuerdo con su complejidad:

| Operador Lógico | Tipo de Compuerta | Representación en Código | Costo Teórico |
| :--- | :--- | :---: | :---: |
| Negación | NOT | `~` | **1** |
| Conjunción | AND | `&` | **2** |
| Disyunción | OR | `\|` | **2** |
| Condicional | Implicación (IF) | `->` | **3** |
| Bicondicional | Equivalencia (IFF) | `<->` | **4** |

### 2. Serie Estática: Costo de Construcción
Representa el costo fijo de fabricación física de la infraestructura del circuito. Analiza la estructura de la expresión (los tokens) de manera determinista sin importar los valores de entrada.
$$Costo_{Construcción} = \sum_{i=1}^{n} Costo(Compuerta_i)$$

### 3. Serie Dinámica: Costo de Operación por Paso
Representa el costo variable en tiempo de ejecución en una sucesión temporal discreta. Evalúa el circuito paso a paso ($t_1, t_2, \dots, t_m$) y acumula **únicamente** el costo de aquellas compuertas intermedias o finales que conmutaron a un estado activo, es decir, cuyo resultado booleano fue **Verdadero (`True`)**.
$$Costo_{Operación\_Total} = \sum_{t=1}^{m} Costo_{paso}(t)$$

---

## 📁 Arquitectura Modular y Separación de Lógicas

El código fuente sigue un diseño funcional altamente desacoplado, dividiendo las responsabilidades en capas claras independientes:

* **Capa de Análisis Gramatical (Parsing):** Convierte expresiones lógicas en formato infijo a Notación Polaca Inversa (RPN) utilizando el algoritmo *Shunting-yard* asistido por pilas (`parse_expression`). Sanitiza y valida las entradas de texto del usuario (`parse_variable_input`).
* **Capa del Motor de Evaluación Lógica (Núcleo):** Evalúa pilas de datos booleanos puros de forma recursiva/iterativa y calcula espacios vectoriales completos (minitérminos) para evaluar equivalencias tautológicas (`evaluate_expression`, `get_minterms`).
* **Capa de Métricas de Series (Corte 3):** Rastrea en tiempo real mediante una pila paralela (`pila_gates`) los estados intermedios de activación lógica para asignar los costos dinámicos por paso de ejecución (`evaluate_with_cost_tracking`).
* **Capa de Interfaz de Usuario (CLI):** Administra la captura de argumentos por línea de comandos mediante la librería estándar `argparse`, encapsulando el lazo continuo de simulación (`while True`) y dándole un formato tabular alineado y legible al reporte final.

---

## 🚀 Guía de Uso de la Nueva Funcionalidad

### Requisitos Previos
* Python instalado en el sistema.

### Comando de Ejecución
Para iniciar el **Modo de Simulación de Secuencias Interactiva**, invoque el script desde la terminal de comandos utilizando el nuevo flag `-si` o `--secuencia-interactiva` acompañado de la expresión lógica deseada entre comillas:

```bash
python logicsim.py -si "(P | ~Q) & P"
