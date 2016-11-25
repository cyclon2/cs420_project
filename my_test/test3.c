float printf(float x, float y){
	return y;	
}

int avg (int count, int value[4]) {
	int total, i, sum;
	int mark[5];
	for (i =0; i < count; i=i+1) {
		int average;
		total = total + value[i];
		mark[i] = i * 30;
		sum = sum + mark[i];
		average = avg(i+1, mark);
		if (average <= 40.0){
			int t,x;
			printf(t,x);	
		}
	}	
	return(total/count);
}
