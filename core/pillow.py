from PIL import Image, ImageDraw, ImageFont
import numpy as np

'''
by default convert a character to a matrix of 1 and 0 with the size of (4 or 5)x6
'''
def chatToMatrix(text, fuente_path='types/Consolas.ttf', tamano_fuente=10, trim = False):
    picture = Image.new('1', (1+int(tamano_fuente/2), tamano_fuente), 0)
    draw = ImageDraw.Draw(picture)
    characters = ImageFont.truetype(fuente_path, tamano_fuente)
    #ancho_texto = characters.getlength(letra)
    #alto_texto = draw.textlength(letra,fuente)
    #alto_texto = tamano_fuente
    draw.text((0, 0), text, fill="white", font=characters)
    # to matrix
    matriz = np.array(picture)

    # if the first column is all 0s, get a new matrix without the first column
    if trim and np.all(matriz[:,0] == 0):
        matriz = matriz[:,1:]
    # if the last column is all 0s, get a new matrix without the last column
    if np.all(matriz[:,-1] == 0):
        matriz = matriz[:,:-1]
    # get a new matrix without the first row, and the last row if they are all 0s
    if np.all(matriz[0,:] == 0):
        matriz = matriz[1:,:]
    if np.all(matriz[-1,:] == 0):
        matriz = matriz[:-1,:]
    #print(matriz)
    return matriz

def iconToMatrix(iconPath, size):
    picture = Image.open(iconPath)
    picture = picture.resize((size, size))
    picture = picture.convert('1')
    matriz = np.array(picture)
    return matriz

if __name__ == '__main__':
    #print(chatToMatrix(':'))
    print(iconToMatrix('icons/arrow.png', 8))
