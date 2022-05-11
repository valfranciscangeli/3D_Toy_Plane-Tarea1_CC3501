# Tarea 02 de Modelación y Computación Gráfica CC3501
-----------------------------------------------------

En esta carpeta se encuentra:

- Carpeta 'assets': donde se encuentran las figuras básicas usadas .off
- Carpeta 'grafica': contiene los módulos que se importan en el 
desarrollo de la tarea.
- model: archivos .mtl y .obj de el modelo elegido para reproducir 
en la tarea. En este caso el modelo elegido es avion 01.
- tarea2_v1.py: archivo python donde se encuentra el desarrollo para 
crear la escena de la tarea.

Para el desarrollo de esta tarea se utilizó como base el código dado
 en el enunciado tarea2_v0.py
Se hacen cambios previos al loop principal para crear el grafo de 
escena que crea al avión. También se agregan transformaciones que cambian en cada ciclo del while correspondiente a la apertura de la ventana.
También se cambia el color de fonde de la ventana para simular cielo
 con el color en RGB (0.447, 0.760, 0.796), alpha= 1.0

Colores en RGB utilizados en la escena, extaidos desde el modelo 
original:
- Cuerpo del avion (verde): (0.000, 0.345, 0.000)
- Soporte de ruedas (anaranjado-marrón): (0.560, 0.286, 0.156)
- Cilindros grises: (0.500, 0.500, 0.500)
- Aspas de helice: (0.100, 0.100, 0.100)
- Además, blanco y negro. 

La escena muestra una animación de 3 aviones, uno más grande en 
el centro y 2 de menor tamaño, donde los 2 menores hacen un giro
en su eje en cierto momento.

- Descomprima los archivos .zip previo a ejecutar el programa. 
