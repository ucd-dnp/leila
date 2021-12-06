.. _datos_gov:

Datos gov
=========

Este módulo permite conectar y evaluar desde el código los metadatos del Portal de Datos Abiertos y descargar las bases de datos a dataframes.

.. warning::
        El módulo de Datos gov utiliza la API de Socrata. Esta permite hacer peticiones para la descarga de datos sin utilizar un token de identificación. Sin embargo, se recomienda crear una cuenta y su respectivo token para evitar que las descargas tengan limitaciones de tamaño y cantidad en los conjuntos de datos.

        La cuenta de usuario puede ser creada desde el portal de `Datos Abiertos de Colombia`_. Es posible solicitar su token con el siguiente enlace `Solicitud token Socrata`_ o también puede tener acceso desde la documentación de API de algún conjunto de datos.

.. _Datos Abiertos de Colombia: https://www.datos.gov.co/signup
.. _Solicitud token Socrata: https://www.datos.gov.co/profile/edit/developer_settings


.. automodule:: datos_gov
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: asset_inventory_espanol

.. include:: ../ejemplos/header_ejemplos.rst
.. include:: ../ejemplos/ejemplos_datos_gov.rst
    :start-line: 3