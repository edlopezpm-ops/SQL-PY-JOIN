# SQL-PY JOIN

Proyecto de practica para reforzar conceptos de SQL Server y Python, con enfoque futuro en una aplicacion SaaS.

## Proposito

Este repositorio servira como base de aprendizaje incremental para:

- Practicar modelado y carga de datos en SQL Server.
- Documentar ejemplos de joins y relaciones entre tablas.
- Integrar posteriormente Python para consultas, automatizacion y APIs.
- Evolucionar el aprendizaje hacia patrones utiles para un futuro producto SaaS.

## Estado actual

El proyecto contiene un script SQL ya ejecutado para crear y poblar una tabla de referencia sobre tipos de joins.

El script es destructivo sólo cuando `@EjecutarCommit` se cambia explícitamente a `Y`: en ese modo crea o vacía `dbo.REGISTER_JOIN` y vuelve a cargar sus filas. El valor versionado permanece en `N`, por lo que la ejecución por defecto termina en rollback.

## Contrato externo

`SP_CreateTables.sql` requiere SQL Server, una base llamada `PYDB` y una tabla existente `dbo.REGISTER` con estas columnas: `INTERNAL_NUM`, `SCRIPT_NAME`, `SCRIPT_TYPE`, `ACTIVE`, `USER_STAMP`, `PROCESS_STAMP` y `DATE_TIME_STAMP`. La validación desechable crea ese contrato con `INTERNAL_NUM = 7` para `SP_CreateTables`.

El bloque `CATCH` revierte la transacción y devuelve el detalle del error como result set, pero no vuelve a lanzar la excepción. Por ello, los consumidores no deben interpretar únicamente el exit code como prueba de éxito; también deben verificar el estado esperado de la base.

## Validar

Requisitos: Bash, Docker y acceso para descargar la imagen oficial de SQL Server fijada en el validator.

```bash
bash tests/validate_sql.sh
```

El validator usa un contenedor efímero, comprueba el rollback predeterminado, ejecuta una copia temporal en modo commit dos veces y verifica filas, claves y recarga idempotente. El contenedor y la contraseña aleatoria se eliminan al salir.

## Alcance futuro

El repositorio podra crecer con ejercicios y componentes relacionados con:

- Conexion Python a SQL Server.
- Consultas parametrizadas y validacion de datos.
- Automatizacion de cargas o reportes.
- APIs con FastAPI.
- Fundamentos reutilizables para una plataforma SaaS.

## Nota

Este es un proyecto de practica y evolucion tecnica. El codigo se mantendra simple, legible y orientado a aprendizaje aplicado.

## Licencia

No existe un archivo de licencia, por lo que este repositorio no concede permiso general para copiar, modificar, distribuir o reutilizar el trabajo. La profesionalización no agregó ni cambió términos de licencia.

## Gobernanza

Los cambios siguen el flujo de ingeniería AEKR: alcance acotado, validación determinista en infraestructura desechable, revisión mediante pull request y recuperación mediante revert PR. La revisión y el merge humanos son obligatorios.
