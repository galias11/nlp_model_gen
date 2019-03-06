# @Classes
from nlp_model_gen.packages.adminModule.AdminModuleController import AdminModuleController

# @Utils
from nlp_model_gen.utils.fileUtils import create_dir_if_not_exist

create_dir_if_not_exist('tmp')
create_dir_if_not_exist('models')

name = "nlp_model_gen"

def NLPModelAdmin():
    return AdminModuleController()
    