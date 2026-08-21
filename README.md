<div align="center">

<img src="src/small/static/small.png" alt="Small" width="96">

# Small

**Frontend alternativo para artículos de Medium**

Fork de [PrivateCoffee/small](https://git.private.coffee/PrivateCoffee/small) con modificaciones propias.

</div>

---

## Qué es esto

Small es un frontend alternativo para Medium escrito en Flask. Permite leer artículos sin la interfaz de Medium, sin JavaScript de terceros y sin telemetría: el servidor pide el contenido a la API GraphQL de Medium y devuelve HTML plano.

Este repositorio es un **fork personal**. El proyecto original es de [Private.coffee](https://private.coffee) y está bajo licencia MIT. Si buscas la versión oficial, ve al repositorio de arriba; aquí solo hay una instancia con cambios adaptados a mi servidor.

## Diferencias respecto al upstream

### Aviso de vista previa en artículos de pago

Upstream pide `content(postMeteringOptions: {})` de forma anónima. En los artículos *member-only* Medium devuelve una vista previa truncada, y Small la renderizaba como si fuera el artículo completo: sin aviso, sin marca, sin nada. El lector no podía distinguir un artículo corto de uno cortado a la mitad.

Este fork añade al query los campos `isLocked`, `visibility`, `mediumUrl` y, dentro de `content`, `isLockedPreviewOnly` y `validatedShareKey`. Cuando el contenido está truncado se muestra un aviso al final indicando cuántos párrafos son vista previa, con enlace al original en Medium.

El aviso dice **vista previa**, nunca *"has agotado tu cuota"*: desde el servidor la respuesta es idéntica cuando se acaba la cuota mensual y cuando nunca hubo acceso, así que afirmar lo segundo sería inventar.

> Los nombres de esos campos se obtuvieron sondeando los mensajes de error del validador GraphQL. La introspección está bloqueada en el endpoint de Medium, tanto `__schema` como `__type`.

### Timeouts en las peticiones salientes

`MediumClient` ya pasaba `timeout=30`, pero el proxy de imágenes y `GithubClient` no llevaban ninguno. Sin timeout, `requests` bloquea indefinidamente y una conexión colgada inmoviliza un worker de uWSGI hasta el reinicio. Un artículo con veinte imágenes puede ocupar varios workers a la vez.

### Tema oscuro único

`style.css` no tenía ninguna custom property: 143 líneas con todos los colores escritos a mano. Se ha introducido la capa de variables (`:root`) y sustituido todos los literales por una paleta oscura. Sin variante clara y sin `prefers-color-scheme`, por coherencia con el resto de servicios de la instancia.

Dos cambios no son sustitución directa: los bloques `pre` tenían `#666` sobre `#f4f4f4`, con mal contraste ya en claro e ilegible en oscuro; y el acento `#1a73e8` no daba contraste suficiente sobre fondo oscuro, así que sube a `#6ea8fe`.

### Interfaz en español

Página de inicio, errores 404 y 500 traducidos, `lang="es"`, y footer que mantiene el crédito a Private.coffee añadiendo el enlace a este fork.

### Favicon

Upstream no declara ninguno, y cada carga generaba un `404` de `/favicon.ico`.

## Uso

Sustituir `https://medium.com/` por la URL de la instancia en cualquier artículo:

- Original: `https://medium.com/@usuario/titulo-123abc`
- Small: `https://small.ejemplo.com/@usuario/titulo-123abc`

## Notas técnicas

Cosas que costaron tiempo y conviene no volver a descubrir:

- **Hay dos clases `Page` en el proyecto.** La que usa `MediumClient` viene de `models/nodes.py`; la de `models/page.py` no la importa nadie. Editar la equivocada produce un `Page.__init__() got an unexpected keyword argument` en tiempo de ejecución mientras el fichero en disco parece correcto.
- **La introspección GraphQL está bloqueada** en `medium.com/_/graphql`, tanto `__schema` como `__type`. Para descubrir campos, enviar el candidato y leer el mensaje de error: el validador suele sugerir el nombre correcto.
- **`PostMeteringOptions` acepta `referrer` y `sk`.** `shareKey` no existe.
- **Werkzeug separa la query string antes del enrutado**, así que el token `sk` de un friend link nunca llega a `parse_article_id`: queda en `request.args`.
- **El paquete se importa desde `site-packages`**, no desde `/app/src`. El `Containerfile` hace `pip install .`, así que verificar cambios con `grep` sobre `/app` puede llevar a conclusiones falsas.
- **`templates/iframe.html` es un fragmento suelto**, sin `<html>` ni enlace al CSS. No hereda de `base.html` y por tanto no recibe los estilos.

## Licencia

MIT, igual que el proyecto original. Ver [LICENSE](LICENSE).

## Créditos

- [Private.coffee](https://private.coffee) por [Small](https://git.private.coffee/PrivateCoffee/small), el proyecto original.
- Inspirado a su vez en [Scribe](https://git.sr.ht/~edwardloveall/scribe).

## Aviso

Proyecto sin relación alguna con Medium, ni respaldado ni patrocinado por ellos.