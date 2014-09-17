    # Perfiles, editar perfil descripcion
def obtener_links_perfil(perfil):
    # Recibe un Perfil object
    # Devuleve una lista con los links.
    def evaluar_link(link, lista):
        # Se asegura que los links sean mas largos que 4 caracteres
        if link is not None:
            lista.append(link)

    link1 = perfil.link1
    link2 = perfil.link2
    link3 = perfil.link3
    link4 = perfil.link4
    link5 = perfil.link5
    links = []

    evaluar_link(link1, links)
    evaluar_link(link2, links)
    evaluar_link(link3, links)
    evaluar_link(link4, links)
    evaluar_link(link5, links)
    return links
