import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from core.ngw_connection_settings import NGWConnectionSettings
from core.ngw_connection import NGWConnection
from core.ngw_resource_factory import NGWResourceFactory

from core.ngw_resource import NGWResource
from core.ngw_vector_layer import NGWVectorLayer

from core.ngw_feature import NGWFeature
from core.ngw_attachment import NGWAttachment

if __name__=="__main__":    
    ngw_resources_id = 1881
    ngw_feature_id = 159
    
    ngwConnectionSettings = NGWConnectionSettings("ngw", "http://demo.nextgis.ru/ngw", "administrator", "admin")
    ngwConnection = NGWConnection(ngwConnectionSettings)    
    ngwResourceFactory = NGWResourceFactory(ngwConnectionSettings)
    
    ngwResource = NGWVectorLayer(ngwResourceFactory, NGWResource.receive_resource_obj(ngwConnection, ngw_resources_id))
    ngwFeature = NGWFeature(ngw_feature_id, ngwResource)
    
    #files = [os.path.join(os.path.dirname(__file__), 'media', 'plaza-1.jpg')]
    files = [
        "d:\\Development\\NextGIS\\D-Day\\foto\\plaza-1.jpg",
        #"d:\\Development\\NextGIS\\D-Day\\foto\\plaza-2.jpg",
        #"d:\\Development\\NextGIS\\D-Day\\foto\\plaza-3.jpg",
        #"d:\\Development\\NextGIS\\D-Day\\foto\\plaza-4.jpg",
        #"d:\\Development\\NextGIS\\D-Day\\foto\\plaza-5.jpg",
        #"d:\\Development\\NextGIS\\D-Day\\foto\\plaza-6.jpg",
             ]
    
    for file_name in files:
        attachment_info = ngwConnection.upload_file( file_name )
        id = ngwFeature.link_attachment(attachment_info)
        print "link attachment with id %s"%str(id)
    
    attachments = ngwFeature.get_attachments()
    for attachment in attachments:
        if attachment[u'is_image'] == True:
            ngw_attachment = NGWAttachment( attachment[u'id'], ngwFeature)
            print ngw_attachment.get_image_full_url()
            #ngwFeature.unlink_attachment( attachment[u'id'] )