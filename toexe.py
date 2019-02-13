#!/usr/bin/python
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

setup(
    name="Tipo De Cambio",
    version="0.1",
    description="Actualiza el correo de forma automatica",
    executables=[Executable("main.py")],
)