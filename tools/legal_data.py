# -*- coding: utf-8 -*-
"""Términos y condiciones de uso del sitio. Mismo formato de bloques que blog_data.py.
IMPORTANTE: borrador preparado con buenas prácticas; debe revisarlo un abogado antes de publicarse,
en especial la cláusula de ley aplicable y jurisdicción."""

PRIVACY = "https://www.1redbrand.com/en/Aviso_de_Privacidad_1RedBrand.pdf"

TERMS = dict(
    updated="2026-11-23",
    title=("Términos y condiciones de uso", "Terms and conditions of use"),
    lede=("Las reglas para usar el sitio www.1redbrand.com. El uso de la plataforma 1RedBrand se rige por el contrato de servicio que firma cada cliente.",
          "The rules for using the www.1redbrand.com website. Use of the 1RedBrand platform is governed by the service agreement each client signs."),
    blocks=[
        ("h2", ("1. Quiénes somos y aceptación", "1. Who we are and acceptance")),
        ("p", ("Este sitio web (el \"Sitio\") es operado por 1RedBrand LLC, sociedad registrada en el estado de Florida, Estados Unidos (\"1RedBrand\", \"nosotros\"). En México, los servicios de 1RedBrand se comercializan a través de Vmasideas.",
               "This website (the \"Site\") is operated by 1RedBrand LLC, a company registered in the state of Florida, United States (\"1RedBrand\", \"we\"). In Mexico, 1RedBrand services are sold through Vmasideas.")),
        ("p", ("Al navegar o usar el Sitio aceptas estos términos. Si no estás de acuerdo con ellos, te pedimos no usar el Sitio.",
               "By browsing or using the Site you accept these terms. If you do not agree with them, please do not use the Site.")),

        ("h2", ("2. Alcance", "2. Scope")),
        ("p", ("Estos términos regulan únicamente el uso del Sitio y de su contenido informativo. La contratación y el uso de la plataforma 1RedBrand y de sus módulos se rigen por el contrato, la propuesta comercial o los términos de servicio que se firmen con cada cliente; en caso de conflicto, prevalece ese documento.",
               "These terms only govern the use of the Site and its informational content. Contracting and using the 1RedBrand platform and its modules are governed by the agreement, commercial proposal or terms of service signed with each client; in case of conflict, that document prevails.")),

        ("h2", ("3. Uso permitido", "3. Permitted use")),
        ("p", ("Puedes usar el Sitio para conocer 1RedBrand, consultar sus contenidos y contactarnos. Al hacerlo te comprometes a no:",
               "You may use the Site to learn about 1RedBrand, read its content and contact us. In doing so you agree not to:")),
        ("ul", [
            ("Usarlo con fines ilícitos o contrarios a estos términos.", "Use it for unlawful purposes or in breach of these terms."),
            ("Intentar acceder sin autorización a sus servidores, archivos o sistemas, o interferir con su funcionamiento.",
             "Attempt to gain unauthorized access to its servers, files or systems, or interfere with its operation."),
            ("Enviar a través del formulario información falsa, de terceros sin su consentimiento, o contenido ofensivo, malicioso o publicitario no solicitado.",
             "Submit false information through the form, third-party information without their consent, or offensive, malicious or unsolicited promotional content."),
            ("Extraer contenido de forma masiva por medios automatizados con fines distintos a la indexación en buscadores o motores de respuesta.",
             "Extract content in bulk by automated means for purposes other than indexing by search or answer engines."),
            ("Copiar, modificar o distribuir el contenido del Sitio fuera de lo permitido en la sección siguiente.",
             "Copy, modify or distribute the Site's content beyond what the next section allows."),
        ]),

        ("h2", ("4. Propiedad intelectual", "4. Intellectual property")),
        ("p", ("La marca 1RedBrand, sus logotipos, el diseño del Sitio, sus textos, imágenes, gráficos y código son propiedad de 1RedBrand o se usan con autorización, y están protegidos por las leyes de propiedad intelectual aplicables.",
               "The 1RedBrand brand, its logos, the Site's design, texts, images, graphics and code are owned by 1RedBrand or used with permission, and are protected by applicable intellectual property laws.")),
        ("p", ("Puedes compartir enlaces al Sitio y citar fragmentos breves indicando la fuente. Cualquier otro uso requiere autorización previa y por escrito. Las marcas de terceros que aparezcan en el Sitio pertenecen a sus respectivos titulares.",
               "You may share links to the Site and quote short excerpts with attribution. Any other use requires prior written permission. Third-party trademarks shown on the Site belong to their respective owners.")),

        ("h2", ("5. Información del Sitio", "5. Information on the Site")),
        ("p", ("El contenido del Sitio es informativo. Las descripciones de módulos, funciones, resultados y casos pueden cambiar sin previo aviso y no constituyen una oferta vinculante. Los resultados de un cliente no garantizan resultados iguales para otro. Las condiciones comerciales aplicables son las de la propuesta o el contrato correspondiente.",
               "The Site's content is for information only. Descriptions of modules, features, results and cases may change without notice and do not constitute a binding offer. One client's results do not guarantee the same results for another. The applicable commercial terms are those of the corresponding proposal or agreement.")),

        ("h2", ("6. Formulario de contacto y datos personales", "6. Contact form and personal data")),
        ("p", (f"Los datos que envías por el formulario se usan para responder tu solicitud y, en su caso, agendar una demostración. Su tratamiento se rige por nuestro <a class=\"link\" href=\"{PRIVACY}\" target=\"_blank\" rel=\"noopener\">aviso de privacidad</a>, que puedes consultar en cualquier momento. Te pedimos enviar solo datos verdaderos y propios.",
               f"The information you send through the form is used to answer your request and, where applicable, schedule a demo. Its processing is governed by our <a class=\"link\" href=\"{PRIVACY}\" target=\"_blank\" rel=\"noopener\">privacy notice</a>, which you can review at any time. Please send only accurate information about yourself.")),

        ("h2", ("7. Cookies y almacenamiento en tu navegador", "7. Cookies and browser storage")),
        ("p", ("El Sitio no usa cookies publicitarias ni de terceros. Solo guarda la información técnica necesaria para funcionar:",
               "The Site does not use advertising or third-party cookies. It only stores the technical information it needs to work:")),
        ("ul", [
            ("<strong>rb-geo</strong> (cookie, 24 horas): el código del país desde el que visitas, para mostrar el Sitio en español o en inglés.",
             "<strong>rb-geo</strong> (cookie, 24 hours): the code of the country you visit from, to show the Site in Spanish or English."),
            ("<strong>rb-lang</strong> (almacenamiento local): el idioma que elegiste con el botón ES/EN.",
             "<strong>rb-lang</strong> (local storage): the language you chose with the ES/EN button."),
            ("<strong>rb-attr</strong> (almacenamiento de sesión, se borra al cerrar la pestaña): el origen de la campaña por la que llegaste, que se adjunta a tu mensaje si nos escribes.",
             "<strong>rb-attr</strong> (session storage, cleared when you close the tab): the campaign you arrived from, attached to your message if you contact us."),
        ]),
        ("p", ("Puedes borrar esta información desde la configuración de tu navegador. Si en el futuro se incorporan herramientas de analítica o publicidad, actualizaremos esta sección y solicitaremos tu consentimiento cuando la ley lo requiera.",
               "You can delete this information from your browser settings. If analytics or advertising tools are added in the future, we will update this section and ask for your consent where the law requires it.")),

        ("h2", ("8. Enlaces a sitios de terceros", "8. Links to third-party sites")),
        ("p", ("El Sitio puede incluir enlaces a sitios que no controlamos. No somos responsables de su contenido, disponibilidad ni prácticas de privacidad; su uso se rige por los términos de cada sitio.",
               "The Site may include links to sites we do not control. We are not responsible for their content, availability or privacy practices; their use is governed by each site's own terms.")),

        ("h2", ("9. Disponibilidad y garantías", "9. Availability and warranties")),
        ("p", ("Procuramos que el Sitio esté disponible y actualizado, pero se ofrece \"tal cual\" y \"según disponibilidad\". No garantizamos que funcione sin interrupciones ni errores, ni que su contenido esté siempre completo o vigente. Podemos modificar, suspender o retirar cualquier parte del Sitio en cualquier momento.",
               "We aim to keep the Site available and up to date, but it is provided \"as is\" and \"as available\". We do not guarantee that it will run without interruptions or errors, or that its content will always be complete or current. We may modify, suspend or remove any part of the Site at any time.")),

        ("h2", ("10. Limitación de responsabilidad", "10. Limitation of liability")),
        ("p", ("En la medida en que la ley aplicable lo permita, 1RedBrand no será responsable por daños indirectos, incidentales o consecuenciales derivados del uso o la imposibilidad de uso del Sitio o de decisiones tomadas con base en su contenido. Nada en estos términos limita derechos que la ley te otorgue como consumidor y que no puedan renunciarse.",
               "To the extent permitted by applicable law, 1RedBrand will not be liable for indirect, incidental or consequential damages arising from the use of, or inability to use, the Site or from decisions made based on its content. Nothing in these terms limits rights you have as a consumer under law that cannot be waived.")),

        ("h2", ("11. Cambios a estos términos", "11. Changes to these terms")),
        ("p", ("Podemos actualizar estos términos. La versión vigente es la publicada en esta página, con su fecha de última actualización. Si sigues usando el Sitio después de un cambio, se entiende que aceptas la nueva versión.",
               "We may update these terms. The version in force is the one published on this page, with its last updated date. If you keep using the Site after a change, you accept the new version.")),

        ("h2", ("12. Ley aplicable y jurisdicción", "12. Governing law and jurisdiction")),
        ("p", ("Estos términos se rigen por las leyes del estado de Florida, Estados Unidos. Cualquier controversia relacionada con el Sitio se someterá a los tribunales competentes de dicho estado, sin perjuicio de los derechos que la legislación de tu país de residencia te reconozca y que no puedan renunciarse.",
               "These terms are governed by the laws of the state of Florida, United States. Any dispute related to the Site will be submitted to the competent courts of that state, without prejudice to any non-waivable rights granted to you by the laws of your country of residence.")),

        ("h2", ("13. Contacto", "13. Contact")),
        ("p", ("Si tienes dudas sobre estos términos, escríbenos a <a class=\"link\" href=\"mailto:hello@1redbrand.com\">hello@1redbrand.com</a>.",
               "If you have questions about these terms, write to us at <a class=\"link\" href=\"mailto:hello@1redbrand.com\">hello@1redbrand.com</a>.")),
    ],
)
