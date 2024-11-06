from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

directorio_credenciales = '/mnt/c/Users/dacab/Desktop/ApiPyDrive/credentials_module.json'

# INICIAR SESION
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

# ENLISTAR LOS PERMISOS ACTUALES
def enlistar_permisos_actuales(id_drive):
    drive = login()
    file1 = drive.CreateFile({'id':id_drive})
    permissions = file1.GetPermissions()
    lista_de_permisos = file1['permissions']

    for permiso in lista_de_permisos:
        # ID DEL PERMISO
        print('ID PERMISO: {}'.format(permiso['id']))
        # ROLE = owner | organizer | fileOrganizer | writer | reader
        print('ROLE: {}'.format(permiso['role']))
        # TYPE (A QUIEN SE LE COMPARTIRA LOS PERMISOS) = anyone | group | user
        print('TYPE: {}'.format(permiso['type']))

        # EMAIL
        if permiso.get('emailAddress'):
            print('EMAIL: {}'.format(permiso['emailAddress']))

        # NAME
        if permiso.get('name'):
            print('NAME: {}'.format(permiso['name']))

        print('=====================================================')

# INSERTAR/ OTORGAR PERMISOS
def insertar_permisos(id_drive,type,value,role):
    drive = login()
    file1 = drive.CreateFile({'id':id_drive})
    # VALUE (EMAIL DE A QUIEN SE LE OTORGA EL PERMISO)
    permission = file1.InsertPermission({'type':type,'value':value,'role':role})

# ELIMINAR PERMISOS
def eliminar_permisos(id_drive,permission_id = None,email = None):
    drive = login()
    file1 = drive.CreateFile({'id':id_drive})
    permissions = file1.GetPermissions()
    if permission_id:
        file1.DeletePermission(permission_id)
    elif email:
        for permiso in permissions:
            if permiso.get('emailAddress'):
                if permiso.get('emailAddress') == email:
                    file1.DeletePermission(permiso['id'])

if __name__ == "__main__":
    id_drive = '0APBB6Yh6HxOcUk9PVA'
    type = 'user'
    value = 'diegosaijannnn@gmail.com'
    role = 'reader'
    permission_id = '03696845346257039923'
    email = 'diegosaijannnn@gmail.com'
    #enlistar_permisos_actuales(id_drive)
    #insertar_permisos(id_drive,type,value,role)
    #eliminar_permisos(id_drive,None,email) 