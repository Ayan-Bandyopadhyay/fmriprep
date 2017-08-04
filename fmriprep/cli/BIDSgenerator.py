import os
import shutil
import sys 
import nibabel as nib
import json



def createBIDS(projDir, pid, visitNum, sessionNum):
    fromDir = projDir + '/data/imaging/participants/' + pid + '/visit' + visitNum + '/session' + sessionNum
    toDirRoot =  '/BIDSproject'
    toDir = '/BIDSproject/sub-01'
    if not os.path.exists(toDir):
        #os.makedirs('my_dataset')
        os.makedirs(toDir)
        os.makedirs(toDir + '/anat')
        os.makedirs(toDir + '/func')
        os.makedirs(toDir + '/dwi')

    ''' Copy over anat '''
    shutil.copyfile(fromDir + '/anatomical/T1w-0_defaced.nii.gz', toDir + '/anat/sub-01_T1w.nii.gz')

    ''' Copy over dwi (incomplete -- missing 2 files)'''
    # shutil.copyfile(fromDir + '/dwi/dwi_raw.nii.gz', toDir + '/dwi/sub-01_dwi.nii.gz')
    # shutil.copyfile(fromDir + '/dwi/dwi_raw.json', toDir + '/dwi/sub-01_dwi.json')


    ''' Copy over func '''
    for root, dirs, files in os.walk(fromDir + '/fmri'):
        taskName = ''
        repTime = 0
        flag = False
        for file in files:
            if(file.endswith('.json')):
                taskName = file.split('.')[0]
                with open(os.path.join(root, file)) as f:    
                    data = json.load(f)
                repTime = data['RepetitionTime']
            if(file == 'task-rest_bold.json'):
                flag = True

        for file in files:
            if(not flag):
                break
            if(file.endswith('.nii.gz')):
                fileName = 'sub-01_' + taskName + '.nii.gz'
                shutil.copyfile(os.path.join(root, file), toDir + '/func/' + fileName)
                toFile = toDir + '/func/' + fileName
                img = nib.load(toFile)
                hdr = img.get_header()
                hdr['pixdim'][4] = repTime
                img.to_filename(img.get_filename())

                ''' Make sure repetition time was saved to nifti file '''
                img = nib.load(toFile)
                assert(img.get_header()['pixdim'][4] == repTime)

            elif(file.endswith('.json')):
                fileName = 'sub-01_' + taskName + '.json'
                shutil.copyfile(os.path.join(root, file), toDir + '/func/' + fileName)              


    ''' Delete the .DS_Store files '''
    # for root, dirs, files in os.walk(toDir):
    #     for file in files:
    #         if(file == '.DS_Store'):
    #             os.remove(os.path.join(root, file))



if(len(sys.argv) == 5):
    createBIDS(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])