<?php
	require("/opt/spt/custom/formatted_emailer/class.phpmailer.php");
	require("/opt/spt/custom/formatted_emailer/class.smtp.php");
	include("/opt/spt/custom/formatted_emailer/valid_email.php");

	date_default_timezone_set("America/Los_Angeles");
	global $To, $From_Name, $From, $Body, $Subject, $CC, $today;
	$today = date("Y-m-d");
	echo $today . "\n";
	$file_name = $argv[1];
	echo "FN = " . $file_name . "\n";
	$To = $argv[2];
	echo "TO = " . $To . "\n";
	$From = $argv[3];
	echo "FROM = " . $From . "\n";
	$From_Name = str_replace('.',' ',$argv[4]);
	echo "FROM_NAME = " . $From_Name . "\n";
	$Subject = str_replace('..',' ',$argv[5]);
	echo "SUBJECT = " . $Subject . "\n";
	#$CC = '';
	$CC = $argv[6];
	echo "CC = " . $CC . "\n";
	$CC_Arr = explode('#Xs*',$CC);
	#print_r($CC_Arr);
	foreach ($CC_Arr as $CC_guy) {
	    echo 'CC GUY = ' . $CC_guy;
	}
        $attachments = array();
	$Body = '';
	$file_handle = fopen($file_name, "r");
	while (!feof($file_handle)) {
	    $line = fgets($file_handle);
            if (strpos($line, 'MATTACHMENT:') !== false) {
                $attachment = str_replace('MATTACHMENT:', '', $line);
                $attachment = preg_replace('~[\r\n]+~', '', $attachment);
                $attachments[] = $attachment;
                echo $attachment;
            } else {
	        #echo $line;
	        $Body .= $line . "\n";
            }
	}
	fclose($file_handle);
	sendMailSent($To,$From_Name,$From,$Body,$Subject,$CC_Arr,$attachments,$today);
	function sendMailSent($To,$From_Name,$From,$Body,$Subject,$CC_Arr,$attachments,$today)
	{
		# Let's valid the email address first
		#$validEmailResult = validEmail($To);
		#echo "validEmailResult = " . $validEmailResult;
		#echo "\nValid Email address found: " . $To . " Return Code for valid email is: " . $validEmailResult . "\n";
		$mail = new PHPMailer();
		$mail->IsSMTP();
		$mail->Host = "mail.2gdigital.com";
		$mail->SMTPAuth = false;
		$mail->From = $From;
		$mail->FromName = $From_Name;
		$mail->AddAddress($To);
                foreach ($CC_Arr as $CC_dude){
                    if ($CC_dude != $To){
		        $mail->AddAddress($CC_dude);
                    }
                }
		$mail->IsHTML(true);
		$mail->Subject = $Subject;
		$mail->Body = $Body; 
                foreach ($attachments as $attachment) {
                    echo "2nd Attachment " . $attachment;
                    $mail->AddAttachment($attachment);
                } 
		if(!$mail->Send())
		{
			echo "Message could not be sent." . "\n";
			echo "Mailer Error: " . $mail->ErrorInfo . "\n\n";
			exit;
		}
	}
	
?>
