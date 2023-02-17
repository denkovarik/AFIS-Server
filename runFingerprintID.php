<?php
require 'Queries.php';

if (isset($_POST['IMG']) || isset($_POST['IMG_TEST'])) 
{
    $extension = ".jpeg";

    if (isset($_POST['IMG'])) {
        #$path = "/var/www/afis-receiver/uploads/";
        $path = "uploads/";
        $basename = "Image_" . time();
        $fullname = $path . $basename . $extension;
        $image = $_POST['IMG'];
    } else {
        echo "Running Test:<br>";
        $basename = "Image_1606625302";
        $fullname = "uploadTest/" . $basename . $extension;
        $image = base64_encode(file_get_contents($fullname));
        #$image = base64_encode(file_get_contents("/var/www/afis-receiver/uploadTest/100_1_10.jpg"));
    }

    // determine the extension of the file
    switch ($image[0]) {
        case "/":
            $extension = ".jpeg";
            break;
        
        default:
            echo "Image Type Not Supported";
            return;
    }

    $decodeImage = base64_decode("$image");
	file_put_contents($fullname, $decodeImage);

    # Make a temp dir for files produced during the automatic 
    # fingerprint recognition
    $tempDir = "temp/";
    !mkdir($tempDir,0777,true);
    echo shell_exec('chmod a+r ' . $tempDir);
    echo shell_exec('chmod a+w ' . $tempDir);
    //$output = shell_exec('python3 source/pythonScripts/processImage.py ' . $fullname . ' ' . $tempDir);

    $tempImName = $tempDir.$basename.".wsq";
    $output = shell_exec('python3 source/pythonScripts/preprocessImage.py ' . $fullname . ' ' . $tempImName);

    $minutiaeFile = $tempDir . $basename . ".xyt";

    // echo shell_exec('./bin/cnvrtIm ' . $fullname . " " . $resizedJpgImName);
    // echo shell_exec('./convertImage.sh');
    echo shell_exec('./runMindtct.sh ' . $tempDir . " " . $tempDir);
    
    echo shell_exec('chmod a+r ' . $minutiaeFile);
    echo shell_exec('chmod a+w ' . $minutiaeFile);
	 
    ### TODO Uncomment to use Database once setup 
    // refresh the list of file paths
    $path_list = 'Datasets/MOLF/DB1_lumidgm/DB1_Lumidgm.lis';
    touch($path_list);
    chmod($path_list, 0777);
    $db_connection = openConnection();
    get_xtyFiles($db_connection, $path_list);   

    ### TODO Comment out next 2 lines on code once database is set up
    # Until Database gets updated 
    #shell_exec("ls Datasets/MOLF/MindtctOutput/DB1_Lumidgm/ | grep .xyt | sed 's%^%Datasets/MOLF/MindtctOutput/DB1_Lumidgm/%g' > Datasets/MOLF/MindtctOutput/DB1_Lumidgm.lis"); 
    $result = shell_exec('./bin/bozorth3 -T 40 -A outfmt=spg -p ' . $minutiaeFile . ' -G ' . $path_list);    
    //$result = shell_exec('./bin/bozorth3 -T 40 -A outfmt=spg -p ' . $minutiaeFile . ' -G Datasets/MOLF/DB1_lumidgm/DB1_Lumidgm.lis');    

    if (empty($result)) {
        echo "None Found";
    } else {
        $result_arr = preg_split('/\s+/', $result);
        foreach($result_arr as $r) {
            // echo result array except for the uploaded file name (redundant info)
            if (strpos($r, "temp") === false) {
                echo basename($r, '.xyt') . ',';
            }
        }
    }


    ### TODO Ask Lane about uncommenting this once database is stepup
    # Delete the filepaths list
    //unlink($path_list);

    ### TODO Comment out this line once everything else is done
    // Delete vv when database setup
    shell_exec("rm " . $path_list);

    # Delete the temp directory
    if (! is_dir($tempDir)) 
    {
        	throw new InvalidArgumentException(
                "$tempDir must be a directory");
    }
    if (substr($tempDir, strlen($tempDir) - 1, 1) != '/') 
    {
       $tempDir .= '/';
    }
        $files = glob($tempDir . '*', GLOB_MARK);
    foreach ($files as $file) 
    {
        if (is_dir($file)) 
        {
            self::deleteDir($file);
        } 
        else 
        {
            unlink($file);
        }
    }
    rmdir($tempDir);
}
?>
