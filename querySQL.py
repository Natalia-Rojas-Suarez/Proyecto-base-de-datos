def delitosSexPorDepartamento():
    return """SELECT d.Nombre_Departamento as departamento, COUNT(DE.ID_caso) as numero_de_delitos
              FROM delitos_sexuales_polic_a_nacional de, departamento d, municipio mc
              WHERE de.codigo_Dane_municipio = mc.codigo_municipio_dane AND mc.codigo_Dane_Departamento = d.Codigo_Dane_Departamento and de.fecha between '2021-02-15' and '2022-01-07'
              GROUP BY (d.Nombre_Departamento)"""



def Grupo_Etario():
    return """SELECT Nombre_Grupo_Etario AS grupo_etario, count(ID_caso) as numeros_casos
              FROM Grupo_Etario ge,Delitos_sexuales_Polic_a_Nacional de
              WHERE ge.ID_grupo_etario =de.id_grupo_etario
              GROUP BY Nombre_Grupo_Etario"""

def genero():
    return """SELECT Nombre_genero AS genero, count(ID_caso) as numeros_casos
              FROM genero gen,Delitos_sexuales_Polic_a_Nacional de
              WHERE gen.ID_genero =de.id_genero
              GROUP BY Nombre_genero"""

def delitosSexPorMunicipio():
    return """SELECT mc.Nombre_Municipio as municipio, COUNT(DE.ID_caso) as  numero_de_delitos
                FROM Delitos_sexuales_Polic_a_Nacional DE, municipio d, municipio mc
                WHERE de.codigo_dane_municipio = mc.Codigo_Municipio_Dane AND mc.Codigo_Dane_Departamento = d.Codigo_Dane_Departamento and de.fecha between '2021-02-15' and '2022-01-07'
                GROUP BY (mc.nombre_municipio)
                ORDER BY (COUNT(DE.ID_caso)) asc"""