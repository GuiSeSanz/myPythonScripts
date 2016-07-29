#!/bin/bash

archivo=*.log

echo ====== $archivo ====== >> Results
echo AC	GO	HSP	IEA	EC	NºSeq	Nºannotations>>Results
resultado1=$(grep 'General: Number of annotated' $archivo | awk '{print $11}')
resultado2=$(grep 'General: Number of annotations' $archivo | awk '{print $10}')
echo $1	$2	$3	$4	$5	$resultado1	$resultado2 >>Results 

