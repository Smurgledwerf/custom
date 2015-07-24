<?php
include 'imdb.php';
$name = $argv[1];
$runner = new Imdb();
$info = $runner->getMultipleMovieInfo($name);
$end_str = '';
if(is_array($info)){
	if(array_key_exists('error',$info)){
		if($info['error'] == "No Title found in Search Results!"){
			$end_str = 'No Titles Found';
		}	
	}
}else{
	$end_str = 'No Titles Found';
}

if(is_array($info)){
	foreach($info as $key=>$arr){
		if(is_array($arr)){
			$end_str.="-MTM_TITLE_MTM-";
                        $top_group = ':-MTM-SUBARRAY-:TopLevel:-::MTM::-';
			if(array_key_exists('error',$arr)){
				if($arr['error'] == "No Title found in Search Results!"){
					$end_str = 'No Titles Found';
				}
			}else{
				foreach($arr as $key=>$val){
					if(is_array($val)){
						$end_str.=":-MTM-SUBARRAY-:$key:-::MTM::-";
						foreach($val as $subkey=>$subval){
							$end_str.=":-MTM-FIELD-:$subkey=>$subval";
						}
					}else{
						$top_group.=":-MTM-FIELD-:$key=>$val";
					}
				}
				$end_str.=$top_group;
			}	
		}else{
			$end_str = 'No Titles Found';
		}
	}
}
echo $end_str;
exit();
?>
