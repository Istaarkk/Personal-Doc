#include <stdio.h>
#include "walktreeid.h"  


void wkt_inorder_show(treeid root) {
    	if (root == 0) {
        	return; 
    	}
    	wkt_inorder_show(wkt_get_left(root));   
    	printf("%c\n", wkt_get_char(root));     
    	wkt_inorder_show(wkt_get_right(root)); 
}

void wkt_postorder_show(treeid root) {
    	if (root == 0) {
        	return; 
    	}
    	wkt_postorder_show(wkt_get_left(root));  
    	wkt_postorder_show(wkt_get_right(root)); 
    	printf("%c\n", wkt_get_char(root));      
}


void wkt_preorder_show(treeid root) {
	if (root == 0) {
        	return; 
    	}
    	printf("%c\n", wkt_get_char(root));  
    	wkt_preorder_show(wkt_get_left(root));  
    	wkt_preorder_show(wkt_get_right(root)); 
}
