{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "netAssociateInstanceIP",
			"Effect": "Allow",
			"Action": "ec2:AssociateAddress",
			"Resource": [
				"arn:aws:ec2:${aws_region}:${account}:instance/*",
				"arn:aws:ec2:${aws_region}:${account}:elastic-ip/${eip-allocation-a}",
				"arn:aws:ec2:${aws_region}:${account}:elastic-ip/${eip-allocation-b}"
			]
		}
	]
}