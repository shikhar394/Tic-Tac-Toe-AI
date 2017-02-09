# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 23:01:33 2016

@author: Shikhar Sakhuja 


Please run the program and just input board positions from 1-9. 
X (AI) goes first. 
"""

import random
class Queue():
    """Queue implementation"""
    class _Node():
        def __init__(self, element, next):
            self.element = element
            self.next = next
            
    def __init__(self):
        self._head = None
        self._tail = None
        
    def enqueue(self, element):
        if self._head == None:
            self._head = self._tail = self._Node(element, None)
        else:
            self._tail.next = self._Node(element, None)
            self._tail = self._tail.next
            
    def dequeue(self):
        if self._head == None:
            raise ValueError
        element = self._head.element
        self._head = self._head.next
        if self._head == None:
            self._tail = None
        return element
        
    def is_empty(self):
        return self._head == None
        
    def front(self):
        if self is None:
            raise ValueError
        return self._head
        
class LinkedTree:
    """Tree Implementation"""
    class Position:
        def __init__(self, container, Node):
            self._container = container
            self._Node = Node
            self._score = 0
            
        def score(self, score):
            """Container for score through minimax"""
            self._score = score
            
        def disp_score(self):
            return self._score
        
        def element(self):
            return self._Node._element   
            
        def __eq__(self, other):
            return type(self) is type(other) and other._Node is self._Node
    
    class _Node:
        def __init__(self, element=None, parent= None, child=None):
            self._element = element
            self._parent  = parent
            self._children = []
            
    def __init__(self):
        self._root = None
        
    def __iter__(self):
        for i in self.breadthFirst():
            yield i
    
    def __str__(self):
        items = []
        for i in self.breadthFirst():
            items.append(i.element())
        return str(items)
        
    def is_empty(self):
        return self._size == 0
        
    def new_root(self, p):
        """To change the root of the tree, used in the play() function to cut down tree possibilities while moving ahead"""
        new_root = self._validate(p)
        self._root._children = new_root._children
        self._root._element = new_root._element
        self._root._parent = None
        self._root = new_root
        return self._root
            
    def root(self):
        if not self.is_empty():
            return self._makePosition(self._root)
        else:
            raise NameError("Tree Empty")
            
    def parent(self, p):
        Node = self._validate(p)
        return self._makePosition(Node._parent)
        
    def siblings(self, p):
        Parent = self.parent(p)
        sibling_list = []
        for i in Parent._Node._children:
            sibling_list.append(i)
        return sibling_list
        
    def is_root(self, p):
        return p == self.root()
        
    def children(self, p):
        Node = self._validate(p)
        return Node._children 
        
    def num_children(self, p):
        Node = self._validate(p)
        return len(Node._children) 
        
    def is_leaf(self, p):
        Node = self._validate(p)
        return len(Node._children) == 0
        
    def depth(self, p):
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))
            
    def height(self, p=None):
        if p == None:
            return self._height_tree(self.root())
        else:
            return self._height_tree(p)
    
    def _height_tree(self, p):
        if self.is_leaf(p):
            return 0
        else:
            return 1+ max(self._height_tree(child) for child in self.children(p))
            
    def add_root(self, element):
        if self._root != None:
            raise NameError("Root already exists")
        self._size =1
        self._root = self._Node(element, None, None)
        return self._makePosition(self._root)
        
        
    def add_child(self, p, element):
        if self._size == 0:
            raise NameError("Empty Tree")
        Node = self._validate(p)
        self._size +=1 
        Node._children.append(self._makePosition(self._Node(element, Node)))
        return Node._children[-1]
        
    def breadthFirst(self):
        if not self.is_empty():
            Fringe = Queue()
            Fringe.enqueue(self.root())
            while not Fringe.is_empty():
                element_pos = Fringe.dequeue()
                yield element_pos
                for child in self.children(element_pos):
                    Fringe.enqueue(child)
                    
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._Node._parent is p._Node:
            raise ValueError('p is no longer valid')
        return p._Node

    def _makePosition(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None
        
        
def check_rows(a):
    """Used in victory board"""
    for i in a:
        if len(set(i)) == 1 and set(i) != {None}:
            return True
    return False
        
def check_diagonals(a):
    """Used in victory board"""
    diagonal1 = []
    diagonal2 = []
    for i in range(len(a)):
        for j in range(len(a[i])):
            if i == j:
                diagonal1.append(a[i][j])
            if i+j == 2:
                diagonal2.append(a[i][j])
    if len(set(diagonal1)) == 1 and set(diagonal1) != {None}:
        return True
    elif len(set(diagonal2)) == 1 and set(diagonal2) != {None}:
            return True
    else:
        return False
    
def check_columns(a):
    """Used in victory board"""
    temp_column = []
    for i in range(len(a)):
        for j in range(len(a[i])):
            temp_column.append(a[j][i])
        if len(set(temp_column)) == 1 and set(temp_column) != {None}:
            return True
        else:
            temp_column = []
    return False
    
def victory_board(cur_board):
    """To check if there is a win or not"""
    if check_rows(cur_board):
        return True
    elif check_columns(cur_board):
        return True
    elif check_diagonals(cur_board):
        return True
    return False
    
def num_elements(cur_board):
    '''Used to check number of non None elements, used in creating children in makeTablePossibilities()
        to find a point where the number of children is more than 5'''
    count = 0
    for i in cur_board:
        for j in i:
            if j != None:
                count +=1
    return count
    
def print_f(cur_board):
    '''Formatted version for printing the tic tac toe table'''
    count = 0
    for i in cur_board:
        if count != 0:
            print('-'*20)
        count +=1
        for j in i:
            if j == None:
                j = '_'
            print(' | ', end='')
            print(j, end=' | ')
        print() 

def makeTablePossibilities(Tree):
    '''Makes the tree with all the table possibilities.'''
    instance = []
    temp = []
    rows = cols = 3
    for i in range(rows):
        for j in range(cols):
            temp.append(None)
        instance.append(temp)
        temp = []
    Tree.add_root(instance)
    total_count = 0
    if not Tree.is_empty():
        Fringe = Queue()
        Fringe.enqueue(Tree.root())
        while not Fringe.is_empty():
            pos = Fringe.dequeue()
            count = num_elements(pos.element())
            if count >=5 and victory_board(pos.element()):
                continue
            else:
                for i in range(len(Tree.root().element())):
                    for j in range(len(Tree.root().element()[i])):
                        cur_board = [k[:] for k in pos.element()]
                        if cur_board[i][j] == None:
                            cur_board[i][j] = 'X' if count % 2 == 0 else 'O' 
                            child = Tree.add_child(pos, cur_board)
                            total_count += 1
                            Fringe.enqueue(child)
        print("Please wait for the program to load")
        return Tree

def minimax(Tree, position):
    '''Implementation of minimax algorithm'''
    if Tree.is_leaf(position):
        if victory_board(position.element()):
            if Tree.depth(position) % 2 == 1:
                    position.score(1)  
            elif Tree.depth(position) % 2 == 0:
                    position.score(-1)  
        return 
    else:
        available_moves = Tree.children(position)
        for positions in available_moves: 
           minimax(Tree, positions)
           if Tree.depth(position) % 2 == 1:
               position.score(min([i.disp_score() for i in Tree.children(position)]))
           else:
               position.score(max([i.disp_score() for i in Tree.children(position)]))
    return 
    
def location(pos):
    '''Converts a single digit indice from an assumed 1D array into an indice for a 2D array'''
    if pos == 1:
        return 0,0
    elif pos == 2:
        return 0,1
    elif pos ==3:
        return 0,2
    elif pos == 4:
        return 1,0
    elif pos == 5:
        return 1,1
    elif pos == 6:
        return 1,2
    elif pos == 7:
        return 2,0
    elif pos == 8:
        return 2,1
    elif pos == 9:
        return 2,2
        
def user_move(Tree, cur_board):
    '''Function for the user move. Used in play function'''
    pos = int(input("Please enter index number to place your marker(1-9)"))
    while pos < 1 or pos>9:
        print("enter a valid number")
        pos = int(input("Please enter index number to place your marker(1-9)"))        
    i,j = location(pos)
    while cur_board[i][j] != None:
        print("Position already taken")
        pos = int(input("Please enter index number to place your marker(1-9)"))        
        i, j = location(pos)      
    cur_board[i][j] = 'O'
    print()
    print('USER MOVE') 
    print()
    print_f(cur_board) 
    print()
    for i in Tree:
        if cur_board == i.element():
            Tree.new_root(i)
    return Tree, cur_board
        
def ai_move(Tree, cur_board):
    '''Function for the computer move. Used in play() function'''
    list_score = ([i for i in Tree.children(Tree.root())])
    wins = []
    draws = []
    for i in list_score:
        if i.disp_score() == 1:
            wins.append(i)
        elif i.disp_score() == 0: 
            draws.append(i)
    if len(wins) > 0:
        score = random.choice(wins) 
    else:
        score = random.choice(draws) 
    score = score.disp_score()
    for i in Tree.children(Tree.root()):
        if score == i.disp_score():
            cur_board = i.element()
            Tree.new_root(i)
    print()
    print('COMPUTER MOVE')
    print()
    print()
    print_f(cur_board)  
    return Tree, cur_board
    
def draw_board(cur_board):
    '''If game is a tie'''
    for i in cur_board:
        for j in i:
            if j == None:
               return False
    return True
            
def play(Tree):
    '''Play function, uses user_move and ai_move to work'''
    cur_board = []
    while not victory_board(cur_board):
        Tree, cur_board = ai_move(Tree, cur_board)
        if victory_board(cur_board):
            print("You lost")
            break
        if draw_board(cur_board):
            print("No one wins")
            break
        Tree, cur_board = user_move(Tree, cur_board)  
        if victory_board(cur_board):
            print("You lost")
            break
        if draw_board(cur_board):
            print("No one wins. It's a draw")
            break
    print("Good Game")
        

    
if __name__ == "__main__":
    MyTree = LinkedTree()
    print("Please wait for the program to load")
    makeTablePossibilities(MyTree)
    minimax(MyTree, MyTree.root())
    play(MyTree)               
