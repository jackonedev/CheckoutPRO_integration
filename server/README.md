![insignia](https://github.com/jackonedev/CheckoutPRO_integration/blob/main/insignia.png?raw=true)

# Introducción

Para la evaluación en cuestión he creado un e-commerce ficticio llamado **Tienda Azul**.
Para ello se ha utilizado claves de acceso, claves públicas y claves de integración de prueba. Por lo que la aplicación solo funciona con cliente de prueba.

**NO INGRESE DATOS PERSONALES**

<br />

# Tech-Stack

- Frontend: 
    - ReactJS
- Backend: 
    - Python 
    - FastAPI 
    - Pydantic 
    - Deta 
    - MercadoPago
- Base de datos: 
    - NoSQL Deta Base
- Despliegue: 
    - Deta Space

# Hands-on

1) ingrsar al link: https://checkoutprotop-1-q9515478.deta.app/
2) completar los 5 fields del formulario utilizando obligatoriamente:
    - email: test_user_36961754@testuser.com
3) Puede utilizar la siguiente tarjeta para pagar:
    - numero: 5031 7557 3453 0604
    - codigo de segurida: 123
    - vencimiento: 11/25
    - nombre: APRO
    - dni: 33555666

<br />

# Special Features

Validación del field teléfono
-

Existen multiples maneras de expresar un número telefónico, la expresión más completa puede ser definida de la siguiente manera:

<center>
    
`telefono = p_i + p_ic + p_ai + codigo_area + p_c + numero    ~ [_1_]`
    
</center>


- p_i: prefijo internacional: +54 54 0054
- p_ic: prefijo internacional para celulares: 9
- p_ai: prefijo acceso interurbanas: 0 (Opcional)
- p_c: prefijo local para celulares: 15
- codigo_area: codigo de area
- numero: numero de la línea

Además suelen existir símbolos auxiliares como espacio o guión -, incluso paréntesis () y símbolo más +

Para comunicarse solo es necesario 10 dígitos, que corresponden a:

<center>
    
`telefono = codigo_area + numero ~ [_2_]`    
    
</center>

A su vez existen códigos de área de dos, tres y cuatro dígitos (ej: 11, 351, 3543).
<br />
<br />
El **validador** elimina todo lo que no sea un número. Cuenta cuantos dígitos numéricos ingresó el usuario, en base a eso depura los posibles patrones fruto de las distintas combinaciones de la expresion `[_1_]`. Una vez que consigue quedarse con los 10 dígitos hace una segunda validación para identificar cada elemento de la expresión `[_2_]`.

Esto se debe a que al crear un **objeto preferencia** en los servidores de Mercado Pago, parte de la información solicitada sobre el comprador debe estar completada en el siguiente formato:

```
"payer": {
        "name": "Juan",
        "surname": "Lopez",
        "email": "user@email.com",
        "phone": {
            "area_code": "11",
            "number": "4444-4444"
        },
```

Por lo tanto por medio de este validador tenemos una comunicación de mejor calidad con el servicio de Mercado Pago.

<br />

# Agradecimientos

A aquellos que me apoyan y para aquellos que me motivan a seguir avanzando. A aquellos que me sirvieron de ejemplo, y a los que me acompañaron durante el camino. Gracias a mí mismo por plantearme objetivos cumplibles y demostrarme estar a la altura de ello. Y por último quiero agradecer a aquellos que me vayan a seguir brindando apoyo y ofreciendo oportunidades para seguir creciendo. Gracias a todos.
