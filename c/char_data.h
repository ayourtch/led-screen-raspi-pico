typedef struct char_data_t {
	char sym;
	char data[48];
} char_data_t;

char_data_t char_data[] = {
    { sym: '.', data: {
        0, 0, 0, 0, 0, 0,  // O   O 
        0, 0, 0, 0, 0, 0,  //      
        0, 0, 0, 0, 0, 0,  //      
        0, 0, 0, 0, 0, 0,  //   O
        0, 0, 0, 0, 0, 0,  //    
        0, 0, 1, 1, 0, 0,  //      
        0, 0, 1, 1, 0, 0,  // O   O
        0, 0, 0, 0, 0, 0,  //      
    } },

{ sym: 'a', data: {
    0, 0, 0, 0, 0, 0,  //      
    0, 0, 0, 0, 0, 0,  //      
    0, 1, 1, 1, 1, 0,  //  OOOO 
    1, 0, 0, 0, 0, 1,  // O    O
    1, 1, 1, 1, 1, 1,  // OOOOOO
    0, 1, 0, 0, 1, 0,  //  O  O
    0, 0, 0, 0, 0, 0,  //      
    0, 0, 0, 0, 0, 0,  //      
} },

{ sym: 'y', data: {
    0, 0, 0, 0, 0, 0,  //      
    0, 1, 0, 0, 0, 0,  //  O   
    0, 0, 1, 1, 0, 0,  //   OO 
    0, 0, 0, 1, 0, 0,  //    O 
    0, 1, 0, 0, 1, 0,  //  O  O
    0, 1, 1, 0, 1, 1,  //   O O 
    1, 1, 0, 0, 1, 1,  // OO  OO
    0, 0, 0, 0, 0, 0,  //       
} },

    { sym: 'A', data: {
        0, 1, 1, 1, 0, 0,  //  OOO  
        1, 0, 0, 0, 1, 0,  // O   O
        1, 0, 0, 0, 1, 0,  // O   O
        1, 1, 1, 1, 1, 0,  // OOOOO
        1, 0, 0, 0, 1, 0,  // O   O
        1, 0, 0, 0, 1, 0,  // O   O
        1, 0, 0, 0, 1, 0,  // O   O
        0, 0, 0, 0, 0, 0,  //      
    } },
    { sym: 'B', data: {
        1, 1, 1, 1, 0, 0,  // OOOO  
        1, 0, 0, 0, 1, 0,  // O   O
        1, 0, 0, 0, 1, 0,  // O   O
        1, 1, 1, 1, 0, 0,  // OOOO 
        1, 0, 0, 0, 1, 0,  // O   O
        1, 0, 0, 0, 1, 0,  // O   O
        1, 1, 1, 1, 0, 0,  // OOOO 
        0, 0, 0, 0, 0, 0,  //      
    } },
    { sym: 'C', data: {
        0, 1, 1, 1, 0, 0,  //  OOO  
        1, 0, 0, 0, 1, 0,  // O   O
        1, 0, 0, 0, 0, 0,  // O    
        1, 0, 0, 0, 0, 0,  // O    
        1, 0, 0, 0, 0, 0,  // O    
        1, 0, 0, 0, 1, 0,  // O   O
        0, 1, 1, 1, 0, 0,  //  OOO  
        0, 0, 0, 0, 0, 0,  //      
    } },
    { sym: 'D', data: {
        1, 1, 1, 0, 0, 0,  // OOO   
        1, 0, 0, 1, 0, 0,  // O  O  
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 1, 0, 0,  // O  O  
        1, 1, 1, 0, 0, 0,  // OOO   
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'E', data: {
        1, 1, 1, 1, 1, 0,  // OOOOO 
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        1, 1, 1, 1, 0, 0,  // OOOO  
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        1, 1, 1, 1, 1, 0,  // OOOOO 
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'F', data: {
        1, 1, 1, 1, 1, 0,  // OOOOO 
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        1, 1, 1, 1, 0, 0,  // OOOO  
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'G', data: {
        0, 1, 1, 1, 0, 0,  //  OOO  
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 1, 1, 1, 0,  // O OOO 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 1, 1, 1, 0, 0,  //  OOO  
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'H', data: {
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 1, 1, 1, 1, 0,  // OOOOO 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'I', data: {
        1, 1, 1, 1, 1, 0,  // OOOOO 
        0, 0, 1, 0, 0, 0,  //   O   
        0, 0, 1, 0, 0, 0,  //   O   
        0, 0, 1, 0, 0, 0,  //   O   
        0, 0, 1, 0, 0, 0,  //   O   
        0, 0, 1, 0, 0, 0,  //   O   
        1, 1, 1, 1, 1, 0,  // OOOOO 
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'J', data: {
        0, 1, 1, 1, 1, 0,  //  OOOO 
        0, 0, 0, 0, 1, 0,  //     O 
        0, 0, 0, 0, 1, 0,  //     O 
        0, 0, 0, 0, 1, 0,  //     O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 1, 1, 1, 0, 0,  //  OOO  
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'K', data: {
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 1, 0, 0,  // O  O  
        1, 0, 1, 0, 0, 0,  // OOO   
        1, 1, 0, 0, 0, 0,  // OOO   
        1, 0, 1, 0, 0, 0,  // O  O  
        1, 0, 0, 1, 0, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  //       
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'L', data: {
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        1, 0, 0, 0, 0, 0,  // O     
        1, 1, 1, 1, 1, 0,  // OOOOO 
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'M', data: {
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 1, 0, 1, 1, 0,  // OO OO 
        1, 0, 1, 0, 1, 0,  // O O O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'N', data: {
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // OO  O 
        1, 1, 0, 0, 1, 0,  // O O O 
        1, 0, 1, 0, 1, 0,  // O  OO 
        1, 0, 0, 1, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  //       
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'O', data: {
        0, 1, 1, 1, 0, 0,  //  OOO  
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 1, 1, 1, 0, 0,  //  OOO  
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'P', data: {
        1, 1, 1, 1, 0, 0, // OOOO
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        1, 1, 1, 1, 0, 0, // OOOO
        1, 0, 0, 0, 0, 0, // O
        1, 0, 0, 0, 0, 0, // O
        1, 0, 0, 0, 0, 0, // O
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: 'Q', data: {
        0, 1, 1, 1, 0, 0, // OOO
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 1, 0, 1, 0, // O O O
        1, 0, 0, 1, 0, 0, // O O
        0, 1, 1, 0, 0, 0, // OOO
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: 'R', data: {
        1, 1, 1, 1, 0, 0, // OOOO
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        1, 1, 1, 1, 0, 0, // OOOO
        1, 0, 1, 0, 0, 0, // O O
        1, 0, 0, 1, 0, 0, // O O
        1, 0, 0, 0, 1, 0, // O   O
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: 'S', data: {
        0, 1, 1, 1, 1, 0, // OOOO
        1, 0, 0, 0, 0, 0, // O
        1, 0, 0, 0, 0, 0, // O
        0, 1, 1, 1, 0, 0, // OOO
        0, 0, 0, 0, 1, 0, // O
        0, 0, 0, 0, 1, 0, // O
        1, 1, 1, 1, 0, 0, // OOOO
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: 'T', data: {
        1, 1, 1, 1, 1, 0,  // OOOOO 
        0, 0, 1, 0, 0, 0,  //     O 
        0, 0, 1, 0, 0, 0,  //     O 
        0, 0, 1, 0, 0, 0,  //     O 
        0, 0, 1, 0, 0, 0,  //     O 
        0, 0, 1, 0, 0, 0,  //     O 
        0, 0, 1, 0, 0, 0,  //       
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'U', data: {
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 1, 1, 1, 0, 0,  //  OOO  
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'V', data: {
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 1, 0, 1, 0, 0,  //  O O  
        0, 1, 0, 1, 0, 0,  //  O O  
        0, 0, 1, 0, 0, 0,  //   O   
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: 'W', data: {
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 0, 0, 1, 0,  // O   O 
        1, 0, 1, 0, 1, 0,  // O O O 
        1, 0, 1, 0, 1, 0,  // O O O 
        1, 1, 0, 1, 1, 0,  // OO OO 
        1, 0, 0, 0, 1, 0,  // O   O 
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: 'X', data: {
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        0, 1, 0, 1, 0, 0, // O O
        0, 0, 1, 0, 0, 0, // O
        0, 1, 0, 1, 0, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: 'Y', data: {
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        1, 0, 0, 0, 1, 0, // O O
        0, 1, 0, 1, 0, 0, // O O
        0, 0, 1, 0, 0, 0, // O
        0, 0, 1, 0, 0, 0, // O
        0, 0, 1, 0, 0, 0, // O
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: 'Z', data: {
        1, 1, 1, 1, 1, 0, // OOOOO
        0, 0, 0, 0, 1, 0,
        0, 0, 0, 1, 0, 0, // O
        0, 0, 1, 0, 0, 0, // O
        0, 1, 0, 0, 0, 0, // O
        1, 0, 0, 0, 0, 0, // O
        1, 1, 1, 1, 1, 0, // OOOOO
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: ' ', data: {
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: ':', data: {
        0, 0, 0, 0, 0, 0, //
        0, 0, 1, 0, 0, 0, //
        0, 0, 1, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 1, 0, 0, 0, //
        0, 0, 1, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: '/', data: {
        0, 0, 0, 1, 0, 0, //
        0, 0, 0, 1, 0, 0, //
        0, 0, 1, 0, 0, 0, //
        0, 0, 1, 0, 0, 0, //
        0, 1, 0, 0, 0, 0, //
        0, 1, 0, 0, 0, 0, //
        1, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: '-', data: {
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 1, 1, 1, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
        0, 0, 0, 0, 0, 0, //
    } },
    { sym: '#', data: {
        0, 1, 0, 1, 0, 0,  // O   O 
        1, 1, 1, 1, 1, 0,  // O   O 
        0, 1, 0, 1, 0, 0,  // O   O 
        0, 1, 0, 1, 0, 0,  // O   O 
        0, 1, 0, 1, 0, 0,  // O   O 
        1, 1, 1, 1, 1, 0,  // O   O 
        0, 1, 0, 1, 0, 0,  // O   O 
        0, 0, 0, 0, 0, 0,  //       
    } },
    { sym: '~', data: {} }
};
