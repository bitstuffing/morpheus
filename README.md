# Morpheus

Morpheus tries to handle Neo to know the real truth of Matrix. 

This project is similar, an implementation of Morpheus, guiding Neo than Matrix is a lie (remember, it's not a Matrix, it's a NeoPixel vector).

Based on a simple hardware (using a Raspberry Pi like controller, in this case the 4 version) easy to understand for anybody, to manage several NeoPixel matrixes from cheap Alibaba sellers and get a working "retro pixel screen", which could be integrated with other projects. 

## Why?

- It's implemented in python, the easiest program language of the world, because you don't have to compile and a kid could easily edit it in the worst pc of the world.
- Have you seen the odd text with other builders/constructor? You have more pixels, do more and better!
- Editors are squared (8x8, 16x16, 32x32...), I want an option with a custom cheap array
- It's opensource, it will work forever.
- You can create plugins and animations, you will be able to import from other works
- There is a web interface to edit animations and other expected actions

# Instalation

You must install the requirements with setup.sh script. It's absoluty neccesary make sure that the installed libraries are just the required ones.

## How it works

There are 256 RGBW neopixel W2812b in each matrix, in 8 fields format per 32 columns. You must take it into account to get the neccesary power for that. 

For that reason you will prefer not use the RPi pins for that, but it's your decission.

For RPi restriction reasons, you must use one of the PWN pins (for that it's configured in the GPIO 12, but you can choose between 12, 13, 18 and 19). 
 
Remember, [you must use the PWN pins](https://pinout.xyz/pinout/pwm)

## Dev. Notes

This project is in investigation phase and it's an early dev. 

It means it doesn't support other configurations and matrix or hardware adquired in other places. If the project has acceptation it could be implemented in the future, but anycase, not now. 

# License

This project, like other released by the author, is licensed under the terms of the [CC BY-NC-ND 4.0](http://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1) license, and developed by [@bitstuffing](https://github.com/bitstuffing) with love. 
