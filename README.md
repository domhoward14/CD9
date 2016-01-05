# CD9
CD9 Project For S.D. I

To Install everything needed for this initial project follow the steps below(asssuming that you are using debian or ubuntu OS)

1.) Switch user to root to properly run the function below
2.) Make sure that you have setuptools if not download this first
3.) Copy and paste the function below
4.) Make sure that you run the function in the same folder where the cd9 requirement list is located or it won't properly work
	function CD9_Install()
	{
		echo "Installing PIP..... "
		echo "\n "
		apt-get install python-pip python-dev build-essential
		echo "\n "
		echo "upgrading PIP to the latest version...."
		pip install --upgrade pip 
		echo "\n "
		echo "installing Django 1.7 ...."
		pip install -U django==1.7
		echo "\n "
		echo "installing dependencies ..."
		pip install -r requiredCD9List.txt
		echo "\n "
		echo "Should be complete.... hopefully !"
	}
