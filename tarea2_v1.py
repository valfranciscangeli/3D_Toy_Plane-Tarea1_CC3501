""""
Primera version completa de la tarea 1
Realizada por Valeria Vallejos Franciscangeli
vvfranciscangeli@gmail.com

Basado en el codigo de Ivan Sipiran para la Tarea 2
Curso CC3501 de la FCFM
Semestre Primavera 2021

Comentado en español
Se dejan los comentarios del código base
Se añaden explicaciones sobre creación del grafo de escena,
fondo de ventana y animaciones

Decidí reproducir la figura Avión 01.
Me llamó la atención ya que parecía un avión de juguete de madera :)

"""

__author__ = "Valeria Vallejos Franciscangeli"
__license__ = "MIT"

# importamos librerias----------
import math
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# EN ESTA SECCION NO SE REALIZAN MODIFICACIONES:---------------------------------------------
# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([10, 10, 10])
        self.camUp = np.array([0, 1, 0])
        self.distance = 10


controller = Controller()


def setPlot(pipeline, mvpPipeline):
    projection = tr.perspective(45, float(width) / float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 5, 5, 5)

    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)


def setView(pipeline, mvpPipeline):
    view = tr.lookAt(
        controller.viewPos,
        np.array([0, 0, 0]),
        controller.camUp
    )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0],
                controller.viewPos[1], controller.viewPos[2])


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_1:
        controller.viewPos = np.array(
            [controller.distance, controller.distance, controller.distance])  # Vista diagonal 1
        controller.camUp = np.array([0, 1, 0])

    elif key == glfw.KEY_2:
        controller.viewPos = np.array([0, 0, controller.distance])  # Vista frontal
        controller.camUp = np.array([0, 1, 0])

    elif key == glfw.KEY_3:
        controller.viewPos = np.array([controller.distance, 0, controller.distance])  # Vista lateral
        controller.camUp = np.array([0, 1, 0])

    elif key == glfw.KEY_4:
        controller.viewPos = np.array([0, controller.distance, 0])  # Vista superior
        controller.camUp = np.array([1, 0, 0])

    elif key == glfw.KEY_5:
        controller.viewPos = np.array(
            [controller.distance, controller.distance, -controller.distance])  # Vista diagonal 2
        controller.camUp = np.array([0, 1, 0])

    elif key == glfw.KEY_6:
        controller.viewPos = np.array(
            [-controller.distance, controller.distance, -controller.distance])  # Vista diagonal 2
        controller.camUp = np.array([0, 1, 0])

    elif key == glfw.KEY_7:
        controller.viewPos = np.array(
            [-controller.distance, controller.distance, controller.distance])  # Vista diagonal 2
        controller.camUp = np.array([0, 1, 0])

    else:
        print('Unknown key')


def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

#----------------------------------------------------------------------------------------------

# Creamos la Escena (3 aviones que se mueven)
def createScene(pipeline):

    #iniciamos las primitivas que necesitamos (hojas): -----------------

    #conos:
    tronco_avion    = createGPUShape(pipeline, bs.createColorConeTarea2(0.000, 0.345, 0.000))
    aleta_avion     = createGPUShape(pipeline, bs.createColorConeTarea2(1.000, 1.000, 1.000))
    aleta_avionY    = createGPUShape(pipeline, bs.createColorConeTarea2(1.000, 1.000, 0.000))
    aleta_avionG    = createGPUShape(pipeline, bs.createColorConeTarea2(0.000, 0.345, 0.000))
    soporterueda    = createGPUShape(pipeline, bs.createColorConeTarea2(0.560, 0.286, 0.156))
    #cubos:
    ala_avion       = createGPUShape(pipeline, bs.createColorCubeTarea2(0.000, 0.345, 0.000))
    #cilindros:
    cola_avion      = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.000, 0.345, 0.000))
    cilindrogris    = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.500, 0.500, 0.500))
    cilindroblanco  = createGPUShape(pipeline, bs.createColorCylinderTarea2(1.000, 1.000, 1.000))
    cilindronegro   = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.000, 0.000, 0.000))
    cilindronaranjo = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.560, 0.286, 0.156))
    #esferas:
    helice_avion    = createGPUShape(pipeline, bs.createColorSphereTarea2(0.100, 0.100, 0.100))
    circuloblanco   = createGPUShape(pipeline, bs.createColorSphereTarea2(1.000, 1.000, 1.000))


    #creamos los nodos: ------------------------------------------------------------------------

    #CUERPO DEL AVION: -------------------------------------------------------
    #---tronco del avion
    nodoTronco = sg.SceneGraphNode('tronco_avion')
    nodoTronco.transform = tr.matmul([tr.scale(1.2,1.2,4.0),
                                      tr.rotationX(np.pi/2)])
    nodoTronco.childs += [tronco_avion]

    #---cola del avion (para que el tronco quede plano)
    nodoCola = sg.SceneGraphNode('cola_avion')
    nodoCola.transform = tr.matmul([tr.rotationX(-np.pi/2),
                                    tr.scale(0.4,4.0,0.4)])
    nodoCola.childs += [cola_avion]

    nodoCola2 = sg.SceneGraphNode('cola_avion2')
    nodoCola2.transform = tr.matmul([tr.translate(0.0, 0.0, 0.2),
                                     tr.rotationX(-np.pi / 2),
                                     tr.scale(0.5, 3.0, 0.5)])
    nodoCola2.childs += [cola_avion]

    nodoCola3 = sg.SceneGraphNode('cola_avion3')
    nodoCola3.transform = tr.matmul([tr.translate(0.0, 0.0, -0.8),
                                     tr.rotationX(-np.pi / 2),
                                     tr.scale(0.6, 3.0, 0.6)])
    nodoCola3.childs += [cola_avion]

    #---modelamos decoracion circular tronco
    nodoDecoTronco = sg.SceneGraphNode("decoracion_tronco")
    nodoDecoTronco.transform = tr.matmul([tr.translate(0.0, 0.0, -3.85),
                                          tr.scale(1.0, 1.0, 0.2),
                                          tr.rotationX(np.pi / 2)])
    nodoDecoTronco.childs += [cilindrogris]

    #---creamos un nodo para juntar todas las partes del tronco
    nodoTroncoCompleto = sg.SceneGraphNode("tronco_completo")
    nodoTroncoCompleto.childs += [nodoTronco,
                                  nodoDecoTronco,
                                  nodoCola,
                                  nodoCola2,
                                  nodoCola3
                                  ]

    #ALAS DEL AVION: -------------------------------------------------------

    #---modelamos una sola ala del avion en tamaño y escala adecuada
    nodoAla = sg.SceneGraphNode("ala_avion")
    nodoAla.transform = tr.matmul([tr.translate(0.0,0.0,-2.0),
                                   tr.scale(5.0,0.12,1.0)])
    nodoAla.childs += [ala_avion]

    #---modelamos ala inferior: se produce por bajar en y la ala de nodoAla
    nodoAlaInf = sg.SceneGraphNode("ala_avion_inf")
    nodoAlaInf.transform = tr.translate(0.0, -0.6, 0.0)
    nodoAlaInf.childs += [nodoAla]

    #---modelamos ala superior: se produce por subir en y la ala de nodoAla
    nodoAlaSup = sg.SceneGraphNode("ala_avion_sup")
    nodoAlaSup.transform = tr.translate(0.0, 1.5, 0.0)
    nodoAlaSup.childs += [nodoAla]

    #---modelamos 1 decoracion circular ala
    nodoDecoAla = sg.SceneGraphNode("decoracion_ala")
    nodoDecoAla.transform = tr.matmul([tr.translate(0.0, 1.505, -2.0),
                                       tr.scale(0.9, 0.12, 0.9)])
    nodoDecoAla.childs += [cilindrogris]

    #---modelamos decoracion circular derecha de ala
    nodoDecoAlaDer = sg.SceneGraphNode("decoracion_ala_der")
    nodoDecoAlaDer.transform = tr.translate(3.9, 0.0, 0.0)
    nodoDecoAlaDer.childs += [nodoDecoAla]

    #---modelamos decoracion circular izquierda de ala
    nodoDecoAlaIzq = sg.SceneGraphNode("decoracion_ala_izq")
    nodoDecoAlaIzq.transform = np.array([
                                        #reflejamos en x (lo vimos en aux 4)
                                        [-1,0,0,0],
                                        [0,1,0,0],
                                        [0,0,1,0],
                                        [0,0,0,1]], dtype = np.float32)
    nodoDecoAlaIzq.childs += [nodoDecoAlaDer]

    #---creamos un nodo que una todas las partes del ala superior
    nodoAlaSupCompleta= sg.SceneGraphNode("ala_sup_completa")
    nodoAlaSupCompleta.transform = tr.translate(0.0,0.5,0.0)
    nodoAlaSupCompleta.childs += [nodoAlaSup,
                                  nodoDecoAlaDer,
                                  nodoDecoAlaIzq]

    #SOPORTES DE ALA: -------------------------------------------------------
    #VERTICALES:
    #---modelamos soporte de ala 1
    nodoSoporteAla1 = sg.SceneGraphNode("soporte_ala1")
    nodoSoporteAla1.transform = tr.matmul([tr.translate(-3.0,0.7,-1.5),
                                           tr.scale(0.03, 1.3, 0.03)])
    nodoSoporteAla1.childs += [cilindronaranjo]

    #---modelamos soporte de ala 2
    nodoSoporteAla2 = sg.SceneGraphNode("soporte_ala2")
    nodoSoporteAla2.transform = np.array([
                                        #reflejamos en x (lo vimos en aux 4)
                                        [-1,0,0,0],
                                        [0,1,0,0],
                                        [0,0,1,0],
                                        [0,0,0,1]], dtype = np.float32)
    nodoSoporteAla2.childs += [nodoSoporteAla1]

    #---modelamos soporte de ala 3
    nodoSoporteAla3 = sg.SceneGraphNode("soporte_ala3")
    nodoSoporteAla3.transform = tr.translate(0.0,0.0,-0.9)
    nodoSoporteAla3.childs += [nodoSoporteAla2]

    #---modelamos soporte de ala 4
    nodoSoporteAla4 = sg.SceneGraphNode("soporte_ala4")
    nodoSoporteAla4.transform = np.array([
                                        #reflejamos en x (lo vimos en aux 4)
                                        [-1,0,0,0],
                                        [0,1,0,0],
                                        [0,0,1,0],
                                        [0,0,0,1]], dtype = np.float32)
    nodoSoporteAla4.childs += [nodoSoporteAla3]

    #---juntamos todos los soportes verticales en un solo nodo
    nodoSoportesVerticales = sg.SceneGraphNode("soportes_verticales")
    nodoSoportesVerticales.childs += [nodoSoporteAla1, #izq atras
                                      nodoSoporteAla2,
                                      nodoSoporteAla3,
                                      nodoSoporteAla4]

    #DIAGONALES:
    #---modelamos soporte de ala 5
    nodoSoporteAla5 = sg.SceneGraphNode("soporte_ala5")
    nodoSoporteAla5.transform = tr.matmul([tr.translate(-1.3,1.2,-1.5),
                                           tr.rotationZ(np.pi/4),
                                           tr.scale(0.03, 1.0, 0.03)])
    nodoSoporteAla5.childs += [cilindronaranjo]

    #---modelamos soporte de ala 6
    nodoSoporteAla6 = sg.SceneGraphNode("soporte_ala6")
    nodoSoporteAla6.transform = tr.translate(0.0, 0.0, -0.9)
    nodoSoporteAla6.childs += [nodoSoporteAla5]

    #---modelamos soporte de ala 7
    nodoSoporteAla7 = sg.SceneGraphNode("soporte_ala7")
    nodoSoporteAla7.transform = np.array([
                                        #reflejamos en x (lo vimos en aux 4)
                                        [-1,0,0,0],
                                        [0,1,0,0],
                                        [0,0,1,0],
                                        [0,0,0,1]], dtype = np.float32)
    nodoSoporteAla7.childs += [nodoSoporteAla5]

    #---modelamos soporte de ala 8
    nodoSoporteAla8 = sg.SceneGraphNode("soporte_ala8")
    nodoSoporteAla8.transform = np.array([
                                        # reflejamos en x (lo vimos en aux 4)
                                        [-1, 0, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], dtype=np.float32)
    nodoSoporteAla7.childs += [nodoSoporteAla6]

    #---juntamos todos los soportes diagonales en un solo nodo
    nodoSoportesDiagonales = sg.SceneGraphNode("soportes_diagonales")
    nodoSoportesDiagonales.childs += [nodoSoporteAla5,
                                      nodoSoporteAla6,
                                      nodoSoporteAla7,
                                      nodoSoporteAla8]

    # RUEDAS DE AVION: -------------------------------------------------------

    #SOPORTES:
    #---modelamos soporte izquierda del avion
    nodoSoporteIzq = sg.SceneGraphNode('soporte_rueda_izq')
    nodoSoporteIzq.transform = tr.matmul([tr.translate(-1.0,-1.5,-2.0),
                                          tr.scale(0.05,0.8,0.8),
                                          tr.rotationX(np.pi )])
    nodoSoporteIzq.childs += [soporterueda]

    #---modelamos soporte derecha del avion
    nodoSoporteDer = sg.SceneGraphNode('soporte_rueda_der')
    nodoSoporteDer.transform = np.array([
                                        # reflejamos en x (lo vimos en aux 4)
                                        [-1, 0, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], dtype=np.float32)
    nodoSoporteDer.childs += [nodoSoporteIzq]

    #---juntamos los dos soportes en un solo nodo
    nodoSoportesRuedas = sg.SceneGraphNode('soportes_rueda')
    nodoSoportesRuedas.childs += [nodoSoporteIzq,
                                  nodoSoporteDer]

    #RUEDAS:

    #---modelamos rueda izquierda del avion
    nodoRuedaIzq = sg.SceneGraphNode('rueda_izq')
    nodoRuedaIzq.transform = tr.matmul([tr.translate(-1.1,-2.2,-2),
                                        tr.scale(0.1, 0.5, 0.5),
                                        tr.rotationZ(np.pi / 2)])
    nodoRuedaIzq.childs += [cilindrogris]

    #---modelamos rueda derecha del avion
    nodoRuedaDer = sg.SceneGraphNode('rueda_der')
    nodoRuedaDer.transform = np.array([
                                        # reflejamos en x (lo vimos en aux 4)
                                        [-1, 0, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], dtype=np.float32)
    nodoRuedaDer.childs += [nodoRuedaIzq]

    #---modelamos la barra que une a las ruedas
    nodoBarra = sg.SceneGraphNode('barra')
    nodoBarra.transform = tr.matmul([tr.translate(0.0, -2.2, -2),
                                     tr.scale(1.0, 0.1, 0.1),
                                     tr.rotationZ(np.pi / 2)])
    nodoBarra.childs += [cilindroblanco]

    #---juntamos ambas ruedas y barra en un solo nodo
    nodoRuedas = sg.SceneGraphNode('ruedas')
    nodoRuedas.childs += [nodoRuedaIzq, nodoRuedaDer, nodoBarra]

    # HELICE DEL AVION:----------------------------------------------

    #---modelamos el centro de la helice
    nodoCentro = sg.SceneGraphNode('centro')
    nodoCentro.transform = tr.matmul([tr.translate(0,0,-2),
                                      tr.scale(0.1,0.1,0.2),
                                      tr.rotationX(np.pi/2)])
    nodoCentro.childs += [cilindronegro]

    #---modelamos aspas de la helice
    nodoAspas = sg.SceneGraphNode('aspas')
    nodoAspas.transform = tr.matmul([tr.translate(0, 0, -2.2),
                                     tr.uniformScale(0.1),
                                     tr.scale(16.0,1.5,0.1)])
    nodoAspas.childs += [helice_avion]

    #---juntamos centro y aspas
    nodoHelice = sg.SceneGraphNode('helice')
    nodoHelice.transform = tr.translate(0,0,-2)
    nodoHelice.childs += [nodoCentro, nodoAspas]

    #---añadimos un nodo para la rotacion de la helice en la animacion
    nodoHeliceRotation = sg.SceneGraphNode('rotacion_helice')
    nodoHeliceRotation.childs+= [nodoHelice]

    # DECORACIONES:-------------------------------------------------------

    #ALETAS TRASERAS DEL AVION:

    nodoAletaBlanca = sg.SceneGraphNode('aleta_blanca')
    nodoAletaBlanca.transform = tr.matmul([tr.translate(0,0.5,3.4),
                                           tr.rotationX(np.pi/6),
                                           tr.shearing(0,0,0,0,0.4,0), #visto en aux 4
                                           tr.scale(0.05,0.8,0.8)])
    nodoAletaBlanca.childs += [aleta_avion]

    nodoAletaAmarilla = sg.SceneGraphNode('aleta_amarilla')
    nodoAletaAmarilla.transform = tr.matmul([tr.uniformScale(0.8),
                                             np.array([
                                                #reflejamos en y (lo vimos en aux 4)
                                                [1,0,0,0],
                                                [0,-1,0,0],
                                                [0,0,1,0],
                                                [0,0,0,1]], dtype = np.float32),
                                             tr.translate(0, 0.4, 4.5),
                                             tr.rotationX(np.pi / 6),
                                             tr.shearing(0, 0, 0, 0, 0.4, 0),  # visto en aux 4
                                             tr.scale(0.05, 0.8, 0.8)])
    nodoAletaAmarilla.childs += [aleta_avionY]

    nodoAletaAzul = sg.SceneGraphNode('aleta_azul')
    nodoAletaAzul.transform = tr.matmul([tr.translate(0,0,2.98),
                                         tr.scale(1.5,0.1,1.0),
                                         tr.rotationX(-np.pi / 2)])
    nodoAletaAzul.childs += [aleta_avionG]

    #CIRCULO QUE SE VE EN EL TRONCO:

    nodoCirculo = sg.SceneGraphNode('circulo_blanco')
    nodoCirculo.transform = tr.matmul([tr.rotationX(np.pi/5),
                                       tr.translate(0, -0.1, -1.7),
                                       tr.uniformScale(0.3),
                                       tr.scale(1, 1, 0.007)])
    nodoCirculo.childs += [circuloblanco]

    # UNIMOS EL CUERPO: ----------------------------------------------------------
    # en caso de que se quiera simular movimiento, vamos a dIvidir el avion final
    # en cuerpo, ruedas y helice
    nodoCuerpo=sg.SceneGraphNode('cuerpo')
    nodoCuerpo.childs += [nodoTroncoCompleto,
                          nodoAlaSupCompleta,
                          nodoAlaInf,
                          nodoSoportesVerticales,
                          nodoSoportesDiagonales,
                          nodoSoportesRuedas,
                          nodoAletaBlanca,
                          nodoAletaAmarilla,
                          nodoAletaAzul,
                          nodoCirculo]

    # RAIZ DEL GRAFO:---------------------------------------------------------

    # armamos el avion pasando todas las partes a el nodo avion

    avion = sg.SceneGraphNode('avion')
    #avion de cabeza:
    #avion.transform = tr.matmul([tr.rotationX(np.pi)]) #descomentar para rotar la vista 180 grados sgn X

    avion.transform = tr.matmul([tr.rotationY(np.pi)]) #descomentar para rotar la vista 180 grados sgn Y
    #avion.transform = tr.matmul([tr.rotationZ(np.pi)]) #descomentar para rotar la vista 180 grados sgn Z
    avion.childs += [nodoCuerpo,
                     nodoRuedas,
                     nodoHeliceRotation]

    #crearemos 3 aviones que se moveran de forma independiente, sirve para animar individualmente
    nodoAvion1 = sg.SceneGraphNode('avion1')
    nodoAvion1.transform = tr.matmul([tr.translate(0,0,-5),tr.uniformScale(0.4)])
    nodoAvion1.childs += [avion]

    nodoAvion1Animado = sg.SceneGraphNode('avion1_animacion')
    nodoAvion1Animado.childs+= [nodoAvion1]

    nodoAvion2 = sg.SceneGraphNode('avion2')
    nodoAvion2.transform = tr.matmul([tr.translate(5,0,-6),tr.uniformScale(0.2)])
    nodoAvion2.childs += [avion]

    nodoAvion2Animado = sg.SceneGraphNode('avion2_animacion')
    nodoAvion2Animado.childs += [nodoAvion2]

    nodoAvion3 = sg.SceneGraphNode('avion3')
    nodoAvion3.transform = tr.matmul([tr.translate(-5,0,-6),tr.uniformScale(0.2)])
    nodoAvion3.childs += [avion]

    nodoAvion3Animado = sg.SceneGraphNode('avion3_animacion')
    nodoAvion3Animado.childs += [nodoAvion3]

    #unimos los 3 aviones en una escena final
    nodoEscena = sg.SceneGraphNode('escena')  #raiz del grafo
    nodoEscena.childs +=[nodoAvion1Animado,
                         nodoAvion2Animado,
                         nodoAvion3Animado]

    return nodoEscena


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 850
    height = 850
    title = "Tarea 2"
    window = glfw.create_window(width, height, title, None, None)



    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline = ls.SimpleGouraudShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.447, 0.760, 0.796, 1.0) #seteamos un color 'celeste', simulando cielo

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    mvpPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    # NOTA: Aqui creas un objeto con tu escena
    dibujo = createScene(pipeline)

    setPlot(pipeline, mvpPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    #configuraciones:
    angulo = 0  # seteamos angulo de giro inicial
    z = 0       # seteamos z inicial

    while not glfw.window_should_close(window):  #ciclo while True si ventana abierta

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        setView(pipeline, mvpPipeline)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        # ANIMACIONES:----------------------------------------

        #---helice que rota en su eje:
        helice=sg.findNode(dibujo, "rotacion_helice")
        helice.transform = tr.rotationZ(-80 *glfw.get_time())

        #---aviones que se mueven:
        z+= 0.02                    #coordenada z del movimiento, aumenta por cada ciclo de ventana
        #print("z:",z)              #descomentar para conocer z
        #avion 1 se traslada derecho por el eje z
        avion1 = sg.findNode(dibujo, 'avion1_animacion')
        avion1.transform = tr.translate(0,0,z)
        #avion 2 y 3 van a trasladarse derecho segun z para dar un giro en el intervalo indicado
        if 15*12*angulo/np.pi<=360 and 2<z:
            #esta condicion dice que rotaran en su eje mientras el angulo de rotacion
            # sea entre 0 y 360, es decir, darán solo 1 vuelta y que hayan pasado z=2
            #se usa la formula de conversion grados-radianes (15*12*angulo/np.pi)
            #se utiliza rotacion segun un eje, para fijar como eje el mismo de los aviones
            #se utiliza translate para que avancen
            #cada avion gira en un sentido diferente (angulo positivo o negativo)

            avion2 = sg.findNode(dibujo, 'avion2_animacion')
            avion2.transform = tr.matmul([tr.rotationAxis(angulo, np.array([5,0,-6]), np.array([5,0,6])),
                                          tr.translate(0, 0, z)])

            avion3 = sg.findNode(dibujo, 'avion3_animacion')
            avion3.transform = tr.matmul([tr.rotationAxis(-angulo, np.array([-5,0,-6]), np.array([-5,0,6])),
                                          tr.translate(0, 0, z)])
            #aumentamos el angulo de rotacion reciencuando se haya entrado en esta condicion, es decir,
            #cuando z sea mayor a 2
            angulo += 0.02               #aumentamos el angulo de rotacion
            # print("angulo:",angulo)    #descomentar para conocer angulo

        else:
            #si todavia no pasamos la cordenada que marca el inicio de la rotacion
            # o terminaron la unica vuelta de giro, seguiran trasladandose derecho segun z
            # se utiliza translate para que avancen
            avion2 = sg.findNode(dibujo, 'avion2_animacion')
            avion2.transform = tr.translate(0, 0, z)

            avion3 = sg.findNode(dibujo, 'avion3_animacion')
            avion3.transform = tr.translate(0, 0, z)


        # DIBUJAMOS LA ESCENA:---------------------------------------------------------
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, pipeline, "model")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()

    glfw.terminate()