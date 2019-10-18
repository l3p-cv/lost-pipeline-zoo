from lost.pyapi import script
import os
from sklearn.cluster import KMeans
import numpy as np
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from keras.models import Model

from keras.preprocessing import image as keras_image

ENVS = ['lost-cv-gpu','lost-cv']
#Lock all resources of a worker when this script is executed. 
#This will prevent worker from executing other scripts while this script is executed.
RESOURCES = ['lock_all'] 
ARGUMENTS = {'n-clusters' : {'value': 20,
                            'help': 'Expected number of clusters - should be equal to number of classes.'}
            }
class ClusterKMeans(script.Script):
    '''This Script clusters all images and requests annotations for each cluster.

    For each image in a folder CNN features are extracted. 
    After that all images will be clustered with KMeans and 
    image annotation will be requested.
    '''
    def main(self):
        n_cluster = int(self.get_arg('n-clusters'))
        self.logger.info('Will load keras model')
        base_model = ResNet50(weights='imagenet')
        self.logger.info('Keras model loaded')
        layer_code = 'avg_pool'
        # base_model.summary()
        model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer_code).output)
        feature_list = []
        img_path_list = []
        self.logger.info('Will compute CNN features')
        for raw_file in self.inp.raw_files:
            media_path = raw_file.path
            media_path = raw_file.path
            file_list = os.listdir(media_path)
            total = float(len(file_list))
            for index, img_file in enumerate(file_list):
                img_path = os.path.join(media_path, img_file)
                img_path_list.append(img_path)
                img = image.load_img(img_path, target_size=(224, 224))
                x = keras_image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)
                # extract features
                features = model.predict(x)
                feature_list.append(features[0].flatten())
                self.update_progress(index*70/total)
        self.logger.info('Computed CNN feature!')
        self.logger.info('Start KMeans clustering')
        kmeans = KMeans(n_clusters=n_cluster, random_state=0).fit(feature_list)
        self.logger.info('Clustering completed!')
        counter = 0
        for sim_class, img_path in zip(kmeans.labels_, img_path_list):
            self.outp.request_annos(img_path, img_sim_class=sim_class)
            self.logger.info('Requested annotation for: {} (cluster: {})'.format(img_path, sim_class))
            counter += 1
            self.update_progress(70 + (counter*30/len(img_path_list)))

if __name__ == "__main__":
    my_script = ClusterKMeans()
