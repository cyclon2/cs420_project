int avg (int count, int value[4]) {
	for (i =0; i < count; i=i+1) { 
				total = total + value[i];
				mark[i] = i * 30;
				sum = sum + mark[i];
 				average = avg(i+1, mark);
				if (average <= 40.0){
					printf(t,x);	
				}
	}	
	return(total/count);
}
