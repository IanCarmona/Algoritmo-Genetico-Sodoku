"Sudoku con algoritmo genético"

El programa fue realizado por:

Carmona Serrano Ian Carlo
Mendez Lopez Luz Fernanda
Perez Lucio Kevyn Alejandro
Rosales Benhumea Aldo

Para ejecutar nuestro código, necesitamos seguir varios pasos:

La primera condición es descargar la carpeta en la que se encuentran los archivos "funciones.py" e "interfaz.py".

Una vez completado el paso anterior, abrir el programa "interfaz.py" y ejecutarlo.

Al abrir la interfaz, podemos observar que es amigable para el usuario, tiene varias opciones que son los botones de las dificultades. Al presionar cualquiera de ellos, genera un sudoku dependiendo de su dificultad y lo muestra en el tablero.

En la parte derecha, podemos encontrar la configuración de parámetros del algoritmo genético. Aquí nos propone algunos valores que se mencionan en el artículo. Los parámetros que se pueden modificar son los siguientes (Porcentaje de cruza 1 y 2, Porcentaje de mutación 1 y 2, Tamaño de la población y Número de generaciones).

Una vez configurados todos los parámetros y seleccionado el sudoku a resolver, podremos hacer clic en el botón "Resolver".

Una vez que el programa esté en ejecución, podrá ver que comienza a trabajar. Es normal que tarde unos cuantos segundos, esto depende del tamaño de la población, pero en promedio es un tiempo de (20 a 30 segundos).

Cada 100 generaciones mostraremos una gráfica de convergencia de cómo se va comportando nuestro programa, el cual mostrará el mejor y el peor individuo de cada generación transcurrida. Al mismo tiempo, el sudoku de esa generación se mostrará en el tablero de la interfaz.

El criterio de paro de nuestro programa son dos, los cuales son que se agoten el número de generaciones ingresadas por medio de la interfaz o que nos devuelva un sudoku válido que debe cumplir la condición de que la aptitud del sudoku sea 0.