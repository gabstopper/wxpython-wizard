
class PanelTracker(object):
    """ Linked List of array objects 
        Use next to retrieve next node in list, previous to get previous node and current to obtain current
        pointer node """
    def __init__(self, listOfObjects):
        self.__panels = listOfObjects   #Keeps track of all panels
        self.__head = None
        self.__tail = None
        self.__pointer = 0              #Pointer to current index
        self.next = None
        self.current = None
        self.previous = None
        self.isFirst = True
        self.isLast = False
        
        if len(self.__panels) > 1:
            self.__head     = self.__panels[0]
            self.__tail     = self.__panels[-1]
            self.__current  = self.__head
        else:
            raise ValueError("Not enough parameters in list, expecting len(list) > 1") 
               
    @property
    def next(self):
        #print "+> Current: %s, Next: %s, pointer->%s" % (self.__current, self.__next, self.__pointer)
        if not self.isLast:                 
            self.__pointer+=1
            self.__next = self.__panels[self.__pointer]
        self.__previous = self.__current    #set current to previous since we are moving the pointer ahead
        self.__current = self.__next        #set new current to next node
        if self.__next == self.__tail:      #flag to check whether this is the tail node
            self.isLast = True
            self.isFirst = False
        else:
            self.isFirst = False
            self.isLast  = False
        return self.__next
    
    @next.setter
    def next(self, value):
        self.__next = value
            
    @property
    def current(self):
        return self.__current
    
    @current.setter
    def current(self, value):
        self.__current = value
    
    @property
    def previous(self):
        #print "-> Current: %s, Previous: %s, pointer->%s" % (self.__current, self.__previous, self.__pointer)
        if not self.isFirst and self.__previous is not None: #previous could be none as initial pointer is on self.__head
            self.__pointer-=1
            self.__previous = self.__panels[self.__pointer] #reset new previous
            self.__next = self.__current
            self.__current = self.__previous
        if self.__previous == self.__head or self.__previous == None:
            self.isFirst = True
            self.isLast = False
        else:
            self.isFirst = False
            self.isLast  = False
        return self.__previous
    
    @previous.setter
    def previous(self, value):
        self.__previous = value
            
if __name__ == "__main__":
    panels = PanelTracker(['panel1', 'panel2', 'panel3', 'panel4', 'panel5'])
    for num in range(1,20):
        if num%3==0:
            for num in range(1,5):
                print "Current: %s, [Previous: %s, First: %s, Last: %s]" % (panels.current, panels.previous, panels.isFirst, panels.isLast)
        else:
            for num in range(1,4):
                print "Current: %s, [Next: %s, First: %s, Last: %s]" % (panels.current, panels.next, panels.isFirst, panels.isLast)
            