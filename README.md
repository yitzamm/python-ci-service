# Laboratorio Final – Pipeline CI con GitHub Actions

## Objetivo

Simular un flujo DevOps completo que cubra desde el desarrollo hasta la integración y despliegue continuo. El proyecto integra buenas prácticas de control de versiones, pruebas automáticas, linting, y ejecución de tests de API mediante Newman.

## Tecnologías

- Control de versiones y CI/CD: Git / GitHub
- Backend: Flask (Python)
- Testing: Pytest para pruebas unitarias, Newman para pruebas de API
- Calidad de código: Lint (Flake8 para Python)
- CI/CD: GitHub Actions

## Flujo de trabajo

### Ramas

- dev: rama de desarrollo, se usa para integración de nuevas funcionalidades.
- main / prod: rama de producción, contiene la versión estable.

### Desarrollo

Para el desarollo del proyecto inicié con varios cambios importantes. En el caso de los disparadores decidí separar el pipeline en 2 flujos de trabajo independientes, uno para las solicitudes de tipo push y otro para los pulls. El pipeline de push CI usa la rama de development y se encarga de realizar los pytests, los API tests y las pruebas de Lint. El pipeline de pull request CI por otra parte, usa la rama de producción, realiza las pruebas de Newman y también genera el artefacto. De esta forma podemos evitar pasos repetitivos o innecesarios, logrando así optimizar tareas y permitir que la infraestructura sea escalable. Aunque este fue uno de los últimos pasos que realicé, fue uno de los primeros puntos que anoté durante la etapa de preparación.

Los comandos que acostumbro a utilizar para inicializar git y hacer el commit inicial son:

// Desde la terminal en la carpeta raíz
1. git init
2. git config --global user.email "email@email.com"
3. git config --global user.name "username"
4. git remote add origin "REPO_URL"
5. git add .
6. git commit -m "Initial commit"
7. git branch -M main
8. git pull origin main --allow-unrelated-histories (si existen commits previos, en mi caso el repositorio remoto tenía los archivos .gitignore y README.md del proyecto)
9. git checkout -b dev
10. git push -u origin dev

La línea branches: [ "main" ] en ci.yml me dió un error de formato: No event triggers defined in on, para arreglarlo lo cambié por:

<img width="425" height="161" alt="Image" src="https://github.com/user-attachments/assets/3f4879c8-4ca3-4b59-80d5-10becc437b3a" />

<img width="565" height="163" alt="Image" src="https://github.com/user-attachments/assets/0ac661d4-bbfe-4330-ab2b-e4120173938f" />

A partir de acá definí no solo el formato de los disparadores sino la lógica de cómo quería que funcionaran y bajo qué rama iba a correr cada uno.

El laboratorio cuenta además con 2 test unitarios para las funciones de add y multiply (agregada en la segunda etapa del proyecto) respectivamente. Sin embargo para que funcionaran tuve que hacerle ciertas correcciones. La primera, crear el archivo __init__.py en la carpeta app/, este archivo le dice a Python que el folder es un paquete y por tanto puede importarse, muy útil en ambientes CI. Adicional, hay que decirle a Python dónde encontrar el módulo de pytest, esto se logra agregando PYTHONPATH=. pytest en ci.yml. Las operaciones add y multiply fueron probados exitosamente usando pytest y también se simularon bugs.

<img width="636" height="240" alt="Image" src="https://github.com/user-attachments/assets/4d400333-bdcb-4a72-b749-d63cfe4a5d94" />

A continuación se nos pidió crear un API usando Flask que regresara una lista de vegetales. En este punto opté por mover las funciones add, multiply y get_vegetables a services.py, y reservar main.py para create_app(), aquí es donde se crea la aplicación Flask y se registran los blueprints. Aparte cree un archivo llamado routes.py para definir las rutas, la lógica de los endpoints y cómo se comportan. En esencia cuando llamamos a main.py para ejecutar Flask, main.py invoca a la función create_app(), una vez creada y configurada routes.py traza la ruta correspondiente. Vale la pena hacer pruebas locales previas al commit cuando sea posible, para este paso cree otro archivo con el nombre run.py, inicialicé el servidor Flask con python run.py en la terminal (carpeta raíz del proyecto) y usé http://localhost:5000/vegetables en el navegador para dar por finalizada la prueba.

<img width="320" height="546" alt="Image" src="https://github.com/user-attachments/assets/5192407b-7d47-4a95-b6df-8108eb413741" />

El siguiente punto a tratar fue la implementación de pruebas lint, pero únicamente en los eventos push. Para estas también realicé pruebas locales en la terminal con python -m flake8, a lo que Lint detectó los siguientes errores de estilo:

<img width="1315" height="682" alt="Image" src="https://github.com/user-attachments/assets/955e79b4-2136-4186-b287-27da5c2910d2" />

Cabe denotar que no es necesario hacer las correcciones a mano, podemos usar Black, un formateador automático por medio de: python -m black . igual en la terminal. Localmente los comandos a ejecutar serían los que se muestran a continuación en dado orden:

- python -m black .
- python -m flake8 .
- python -m bandit -r app
- python -m pytest

Tras corregir los problemas de formato y estilo, incorporé Format check (black) y Lint (flake8) dentro de push-ci.yml, recordemos que el objetivo sigue siendo la automatización del pipeline. Finalmente, correspondía agregar las pruebas Newman a los eventos pull antes de un merge. Esta fue la sección en la que más demoré y la que más correcciones necesitó. En seguida, abordaré los conflictos a los que me enfrenté y cómo solucioné cada uno. Aunque no era requisito generar un artefacto como parte del proyecto, sí fue un concepto que vimos en clase y aproveché esta oportunidad para investigar más de fondo. El primer error fue: This request has been automatically failed because it uses a deprecated version of actions/upload-artifact: v3. Este fue sencillo de corregir, simplemente era cuestión de actualizar la versión que estaba usando del artifacto de actions/upload-artifact@v3 (decomisionada) a actions/upload-artifact@v4. En el segundo pull request obtuve Error: collection could not be loaded, ENOENT: no such file or directory. En efecto, no tenía creado el archivo collection.json en el directorio postman/. El path para correr los Newman API tests debía ser entonces newman run postman/collection.json. En seguida, me regresó Error: the file at "postman/collection.json" does not contain valid JSON data. Con este log confirmé que Python sí logró encontrar el archivo mas no pudo validarlo pues no había contenido para validar. Como no tenía ningún test para correr, usé un ejemplo genérico con formato JSON válido para evitar cualquier No data, empty error. Llegando al cuarto y último pull antes del merge, finalmente obtuve luz verde de la prueba Newman y del artefacto, pero aún así hubo un error con el certificado SSL: unable to get local issuer certificate. Debido a que se trata de un CI testing, le puedo decir a Newman que ignore la certificación: newman run postman/collection.json --insecure --reporters cli,junit --reporter-junit-export newman-results.xml. El parámetro --insecure me permite forzar el bypass del certificate validation en entornos de prueba.

<img width="616" height="102" alt="Image" src="https://github.com/user-attachments/assets/3e317001-5e7e-42b9-b71f-2e8fefb95eab" />

### Revisión y pruebas

Los pull requests incluyen revisiones de código y ejecución de tests automáticos.

Se ejecutan:

- Pytest → pruebas unitarias del backend (push).
- Lint → análisis de calidad de código (push).
- Newman → pruebas de API basadas en la colección de Postman (pull).

Tan pronto como el pipeline consigue pasar las pruebas de pytest, API, lint y Newman puedo aprobar el merge a prod/main y continuar con el desarrollo de nuevos features para el aplicativo. En escenarios reales, la aprobación le correspondería al supervisor autorizado.

Como punto final agregué un scanner de seguridad al proyecto usando Bandit. Bandit utiliza 3 niveles de confidencialidad y severidad para etiquetar errores potenciales y señalar malas prácticas: Low, Medium y High. Sin embargo, no quería que el escaneo detuviera el pipeline a menos de que el error fuera crítico entonces cambié bandit -r . (scan básico) por bandit -r . -lll --exit-zero. El problema esque los logs no muestran un registro detallado de los errores y tampoco generan ningún reporte, por lo que resulta difícil saber dónde se encuentra la brecha y qué tan grave es. Para generar un reporte manteniendo la restricción anterior podemos usar: bandit -r . -f json -o bandit_report.json -lll. Es buena práctica usar artefactos para gestionar estos reportes como lo hicimos con las pruebas de Newman, bajo esa misma lógica podemos mandar a subir el bandit report a un segundo artefacto desde el pipeline de push.

<img width="1551" height="213" alt="Image" src="https://github.com/user-attachments/assets/ea52542f-0a0d-46b4-88db-14454dcc7570" />

### Integración y despliegue

Los cambios aprobados en dev se pueden mergear a main/prod. Se mantiene un flujo CI/CD que asegura que todo commit en dev o PR hacia main pase las pruebas antes del despliegue.

## Preguntas de reflexión

### ¿Qué detiene el pipeline?

El pipeline se detiene cuando alguna de las etapas falla, por ejemplo si Pytest detecta errores en los test unitarios, si Lint o Black detectan problemas de estilo o de formato, o si Newman encuentra errores en las pruebas de API como endpoints rotos o certificados inválidos. En general, cualquier fallo en pruebas automáticas o checks de calidad bloquea la continuación hasta que se corrija el error.

### ¿Qué evidencia deja CI?

CI genera registros y reportes automáticos que muestran:

- Resultados de tests unitarios (Pytest).
- Resultados de tests de API (Newman), incluyendo conteo de requests ejecutadas y fallidas.
- Reportes de lint/format (errores de estilo o código no formateado).
- Artefactos generados (por ejemplo, archivos XML con resultados de Newman).

Esto permite verificar de manera objetiva si los cambios cumplen con los estándares antes de mergear a producción.

### ¿Por qué este flujo escala bien en equipos grandes?

- Cada desarrollador trabaja en feature branches aisladas.
- Los pipelines se ejecutan automáticamente en push y pull requests, detectando errores temprano.
- La separación de rama dev y rama main/prod permite integrar cambios sin interrumpir la versión estable.
- La automatización evita pasos repetitivos y asegura consistencia en pruebas, estilo y despliegue, facilitando la colaboración de múltiples equipos simultáneamente.