import numpy as np

class Buffer:

    def __init__(self):
        self.DIMENSION = 8
        self.SCREENS = 8 # 4 panels of 8x8 pixels
    
    def rotateWithoutPillow(self, buffer, rows=8, columns=8):
        buffer2 = [(0, 0, 0) for _ in range(rows * columns)]
        
        matriz = []
        
        for _ in range(rows):
            fila = [[0, 0, 0] for _ in range(columns)]
            matriz.append(fila)
        
        for i in range(rows):
            for j in range(columns):
                matriz[j][i] = buffer[i * rows + j]

        for i in range(rows):
            for j in range(columns):
                if i % 2 == 0:
                    buffer2[i * rows + j] = matriz[rows - j - 1][i]
                else:
                    buffer2[i * rows + j] = matriz[j][i]
        
        return buffer2



    def rotateWithoutPillow2(self, buffer, rows = 8, columns = 8):
        #instance a new buffer
        buffer2 = [(0, 0, 0) for _ in range(rows*columns)]
        #parse buffer to a matrix
        
        matriz = np.array(buffer).reshape(columns, rows, 3)
        #rotate matrix
        matriz_rotada = np.rot90(matriz, 1)
        #parse matrix to buffer
        for i in range(rows):
            for j in range(columns):
                if i%2 == 0:
                    buffer2[i*rows+j] = matriz_rotada[i][j]
                else:
                    buffer2[i*rows+j] = matriz_rotada[i][rows-j-1]
        
        return buffer2

    # just works with 8x8 matrix, needs to be regular matrix
    def rotate(self, buffer):
            
        buffer2 = np.array(buffer)
        matriz = buffer2.reshape(self.DIMENSION, self.DIMENSION, 3) # 3 = red + green + blue
        matriz_rotada = np.rot90(matriz, 1)

        for i in range(self.DIMENSION):
            for j in range(self.DIMENSION):
                if i%2 == 0:
                    buffer[i*self.DIMENSION+j] = matriz_rotada[i][j]
                else:
                    buffer[i*self.DIMENSION+j] = matriz_rotada[i][self.DIMENSION-j-1]
        return buffer
    
    def mirrorWithoutPillow(self, buffer, rows = 8, columns = 32):
        buffer2 = [(0, 0, 0) for _ in range(rows*columns)]
        for i in range(columns):
            for j in range(rows):
                buffer2[i*rows+j] = buffer[rows*(columns-1-i)+(rows-1-j)]
        return buffer2
    
    # just works with 8x8 matrix, needs to be regular matrix
    def mirror(self, buffer):
        size = len(buffer)
        #root of size
        root = int(size**0.5)
        #print(root)
        buffer2 = [(0, 0, 0) for _ in range(root*root)]
        #print(f"buffer2 size: {len(buffer2)}")
        
        #matriz_espejo = np.flip(matriz, axis=1)
        try:
            for i in range(root): # column
                for j in range(root): # field
                    if i%2 == 0 or True:
                        buffer2[i*root+j] = buffer[root*(root-1-i)+(root-1-j)]
                        
        except Exception as e: 
            print(f"error in i={i} and j={j} with root={root} and size={size}")
            print(e)
        '''
        buffer2 = np.array(buffer2)
        matriz = buffer2.reshape(root, root, 3)
        matriz_rotada = np.invert(matriz)
        buffer2 = matriz_rotada.flatten()
        '''
        return buffer2
