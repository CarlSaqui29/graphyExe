from ui import * # import GUI design
from PyQt5.QtWidgets import * # import all PYQT5 Widgets
import sys
from pprint import pprint # use is progressbar
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QBasicTimer # timer for progressbar count

class Vertex: #
    def __init__(self, n):
        self.name = n
        self.neighbors = list()
        self.distance = 9999
        self.color = 'black'

        self.discovery = 0
        self.finish = 0

    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()

class Ui_MainWindow(Ui_MainWindow, QMainWindow):
    vertices = {} # init vertices, where all vertex is stored
    time = 0
    def __init__(self, graph = None):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        # init graph
        if graph is None:
            graph = {}
        self.graph = graph

        # init message boxes
        # for error handling purposes
        self.msg = QMessageBox()
        self.msg.setWindowTitle('Error Occur')
        self.msg.setIcon(QMessageBox.Critical)

        self.del_msg = QMessageBox()
        self.del_msg.setWindowTitle('Confirm')
        self.del_msg.setIcon(QMessageBox.Warning)

        self.timer = QBasicTimer()
        self.step = 1 # init step for progressbar
        self.frame.show()
        self.timer.isActive() # activate timer
        self.timer.start(100, self)
        self.dot = ['', '.', '..', '...', '....', '.....', '......'] # use in loading text
        self.dot_i = 0

        self.index_vertex = 0  # index for vertex_list
        self.added_edge = 0  # when and edge is added it will increment
        self.indexing = 0
        self.i = 0
        self.vertex_list = []  # where vertex is inserted
        self.empty_status = []  # [0,0] to be inserted in status
        self.status = []  # [[0,0], [0,0]] the status of vertices
        self.storage_list = []  # where updated status is inserted and not to be edited
        self.edges = []

        # radio buttons functions
        self.rb_show_ttb.setChecked(True)
        self.rb_show_bfs.setChecked(False)
        self.rb_show_dfs.setChecked(False)
        self.rb_show_ttb.clicked.connect(self.print_truth_table)
        self.rb_show_bfs.clicked.connect(self.print_bfs_)
        self.rb_show_dfs.clicked.connect(self.print_dfs_)

        self.BFS_container.hide()
        self.DFS_container.hide()
        self.add_vertex_container.hide()
        self.add_edge_container.hide()

        # init buttons as disabled
        # enable when lineedit is not empty
        # or list not empty
        self.pb_add_vertex.setDisabled(True)
        self.pb_add_edge.setDisabled(True)
        self.pb_bfs.setDisabled(True)
        self.pb_dfs.setDisabled(True)
        self.pb_delete_all.setDisabled(True)

        # init list widget to empty text
        self.listWidget_2.addItem('Nothing to show...')
        self.listWidget.addItem('Nothing to Show (Edge Truth Table)')

        # signals and slots/events
        self.lineedit_vertex.textChanged.connect(self.check_vertex)
        self.lineedit_edge_one.textChanged.connect(self.check_edge)
        self.lineedit_edge_two.textChanged.connect(self.check_edge)
        self.lineedit_bfs.textChanged.connect(self.check_bfs)
        self.lineedit_dfs.textChanged.connect(self.check_dfs)
        self.comboBox.currentIndexChanged.connect(self.menu)
        self.pb_add_vertex.clicked.connect(self.add_vertex)
        self.pb_add_edge.clicked.connect(self.add_edge)
        self.pb_bfs.clicked.connect(self.print_bfs)
        self.pb_dfs.clicked.connect(self.dfs_)
        self.pb_delete_all.clicked.connect(self.delete_all)
        self.del_msg.buttonClicked.connect(self.action)

    def timerEvent(self, event): # progressbar function
        if self.step == 100: # if progressbar is full, hide progressbar
            self.frame.hide()
        if self.step >= 0 and self.step < 25: # if progressbar is in 1/4 to full
            self.label_19.setText('Initializing Environment' + self.dot[self.dot_i])
            self.dot_i += 1
            # dot animation
            if self.dot_i == 7:
                self.dot_i = 0
        if self.step >= 25 and self.step < 50: # if progressbar is in 2/4 to full
            self.label_19.setText('Preparing PyQt Widgets' + self.dot[self.dot_i])
            self.dot_i += 1
            # dot animation
            if self.dot_i == 7:
                self.dot_i = 0
        if self.step >= 50 and self.step < 80: # if progressbar is in 3/4 to full
            self.label_19.setText('Cleaning-Up database' + self.dot[self.dot_i])
            self.dot_i += 1
            # dot animation
            if self.dot_i == 7:
                self.dot_i = 0
        if self.step >= 80 and self.step < 100: # if progressbar is near to full
            self.label_19.setText('Getting started' + self.dot[self.dot_i])
            self.dot_i += 1
            # dot animation
            if self.dot_i == 7:
                self.dot_i = 0
            # update text pos when text changed
            self.label_19.setGeometry(330, 590, 281, 31)
            self.label_21.setGeometry(300, 590, 21, 31)
        self.step = self.step + 1 # increment step of progressbar
        self.progressBar.setValue(self.step)

    def add_vertex_(self, vertex): # add vertex method 1 param (vertex)
        # if vertex entered is not exist in vertices add vertex
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex

    def add_edge_(self, u, v): # add edge method 2 param (vertex1, vertex2)
        # if 2 vertex exist in vertices list
        # add edge
        if u in self.vertices and v in self.vertices:
            for key, value in self.vertices.items():
                if key == u:
                    value.add_neighbor(v)
                if key == v:
                    value.add_neighbor(u)

    def _dfs(self, vertex): # depth first traversal
        # colors just for text indicator
        global time
        vertex.color = 'red'
        vertex.discovery = time # discovery time
        time += 1
        for v in vertex.neighbors:
            if self.vertices[v].color == 'black':
                self._dfs(self.vertices[v])
        vertex.color = 'blue'
        vertex.finish = time
        time += 1

    def dfs(self, vertex): # receives the source vertex and pass to _dfs() to start to search
        global time
        time = 1
        self._dfs(vertex)

    def print_dfs_(self): # no edges traversing
        self.listWidget.clear()
        if self.index_vertex == 0:
            self.listWidget.addItem('Nothing to Show (DFS Traversal)')
        elif self.index_vertex > 0 and self.added_edge == 0:
            self.listWidget.addItem('Vertex ---> Edges ---> Discovery Time(DT)/ Finished Time(FT)')
            self.listWidget.addItem('Sorted')
            for i in range(len(self.vertex_list)):
                self.add_vertex_(Vertex(self.vertex_list[i]))
            for key in sorted(list(self.vertices.keys())):
                self.listWidget.addItem(key + ' ---> [] ---> 0/0')
            self.lineedit_dfs.clear()
        else:
            self.rb_show_dfs.setChecked(True)
            self.neighbors = list()
            self.vertices = {}
            self.discovery = 0
            self.finish = 0
            self.color = 'black'
            self.listWidget.clear()

            for i in range(len(self.vertex_list)):
                self.add_vertex_(Vertex(self.vertex_list[i]))
            for edge in self.edges:
                self.add_edge_(edge[:1], edge[1:])

            self.listWidget.addItem('Vertex ---> Edges ---> Discovery Time(DT)/ Finished Time(FT)')
            self.listWidget.addItem('Sorted')
            for key in sorted(list(self.vertices.keys())):
                self.listWidget.addItem(key + ' ---> ' + str(self.vertices[key].neighbors) + " ---> 0/0")
            self.lineedit_dfs.clear()

    def dfs_(self): # traversing using dfs
        # discovery time is time when vertex is discover (assume 1 count as 1 sec)
        # finished time is time when search is going back to source vertex
        # eg.
        # source vertex = a
        # a has an edge with b so..
        # a --> b
        # start search, since a is source
        # discovery time of a is 1, proceed...
        # since b is edge of a discovery time of b is 2
        # now b has no edge so the search is going back so..
        # b has the finished time of 3
        # and a has finished time of 4
        # -->1 a -->2 b  // discovery time
        # a 4<-- b 3<--  // finished time
        # a 1/4, b 2/3
        text = self.lineedit_dfs.text()
        # error handling if vertex is equal to 0
        if self.index_vertex == 0:
            self.msg.setText('Please add vertex first!')
            self.msg.exec_()
            self.lineedit_dfs.clear()
        # error handling if vertex inputted by user is not exist in vertices
        elif text not in self.vertex_list:
            self.msg.setText("No vertex '" + text + "' in Vertices!")
            self.msg.exec_()
            self.lineedit_dfs.clear()
        else:
            self.rb_show_dfs.setChecked(True)
            self.neighbors = list()
            self.vertices = {}
            self.discovery = 0
            self.finish = 0
            self.color = 'black'
            self.listWidget.clear()
            text = self.lineedit_dfs.text()
            a = Vertex(text)
            self.add_vertex_(a)

            for i in range(len(self.vertex_list)):
                self.add_vertex_(Vertex(self.vertex_list[i]))
            for edge in self.edges:
                self.add_edge_(edge[:1], edge[1:])

            self.dfs(a)
            self.listWidget.addItem('Vertex ---> Edges ---> Discovery Time(DT)/ Finished Time(FT)')
            self.listWidget.addItem('Sorted')
            for key in sorted(list(self.vertices.keys())):
                self.listWidget.addItem(key + ' ---> ' + str(self.vertices[key].neighbors) + " ---> " + str(self.vertices[key].discovery) +'/'+str(self.vertices[key].finish))
            self.lineedit_dfs.clear()

    def bfs_(self, vert): # breadth first traversal
        q = list()
        vert.distance = 0
        vert.color = 'red'
        for v in vert.neighbors:
            self.vertices[v].distance = vert.distance + 1
            q.append(v)

        while len(q) > 0:
            u = q.pop(0)
            node_u = self.vertices[u]
            node_u.color = 'red'

            for v in node_u.neighbors:
                node_v = self.vertices[v]
                if node_v.color == 'black':
                    q.append(v)
                    if node_v.distance > node_u.distance + 1:
                        node_v.distance = node_u.distance + 1

    def print_bfs_(self):# when rb_show_bfs clicked
        self.listWidget.clear()
        # error handling, if vertex is null
        if self.index_vertex == 0:
            self.listWidget.addItem('Nothing to Show (BFS Traversal)')
        # error handling if there is no edges between vertex display 9999 to distance
        elif self.index_vertex > 0 and self.added_edge == 0:
            self.listWidget.addItem('Vertex ---> Edges ---> Distance to the Source')
            self.listWidget.addItem('Sorted')
            for i in range(len(self.vertex_list)):
                self.add_vertex_(Vertex(self.vertex_list[i]))
            for key in sorted(list(self.vertices.keys())):
                self.listWidget.addItem(key + " ---> [] ---> 9999")
            self.lineedit_bfs.clear()
        else:
            self.rb_show_bfs.setChecked(True)
            self.neighbors = list()
            self.vertices = {}
            self.distance = 9999
            self.color = 'black'
            self.listWidget.clear()

            for i in range(len(self.vertex_list)):
                self.add_vertex_(Vertex(self.vertex_list[i]))
            for edge in self.edges:
                self.add_edge_(edge[:1], edge[1:])
            self.listWidget.addItem('Vertex ---> Edges ---> Distance to the Source')
            self.listWidget.addItem('Sorted')
            for key in sorted(list(self.vertices.keys())):
                self.listWidget.addItem(key + ' ---> ' + str(self.vertices[key].neighbors) + " ---> 9999")
            self.lineedit_bfs.clear()

    def print_bfs(self):
        # bfs traversal is finding the distance of the specific vertex from the source
        # eg..
        # source = a
        # a has a edge of b so...
        # a --> b
        # since a is source the distance of a is 0
        # and the distance of b is 1 since it is edged to a
        # if we add edge to b, like c so..
        # a --> b --> c
        # the distance of c to source which is a is 2
        # a --> b --> c
        # 0 --> 1 --> 2
        # but how about if a has a new edge letter d so..
        # a --> b, d --> c
        # 0 --> 1 --> 2
        # still the distance of d is 1 because it is edge of source
        text = self.lineedit_bfs.text()
        if self.index_vertex == 0:
            self.msg.setText('Please add vertex first!')
            self.msg.exec_()
            self.lineedit_bfs.clear()
        elif text not in self.vertex_list:
            self.msg.setText("No vertex '" + text + "' in Vertices!")
            self.msg.exec_()
            self.lineedit_bfs.clear()
        else:
            self.rb_show_bfs.setChecked(True)
            self.neighbors = list()
            self.vertices = {}
            self.distance = 9999
            self.color = 'black'
            self.listWidget.clear()
            text = self.lineedit_bfs.text()
            a = Vertex(text)
            self.add_vertex_(a)

            for i in range(len(self.vertex_list)):
                self.add_vertex_(Vertex(self.vertex_list[i]))
            for edge in self.edges:
                self.add_edge_(edge[:1], edge[1:])

            self.bfs_(a)
            self.listWidget.addItem('Vertex ---> Edges ---> Distance to the Source')
            self.listWidget.addItem('Sorted')
            for key in sorted(list(self.vertices.keys())):
                self.listWidget.addItem(key + ' ---> ' + str(self.vertices[key].neighbors) + " ---> " + str(self.vertices[key].distance))
            self.lineedit_bfs.clear()


    def check_vertex(self): # check lineedit of add vertex if empty or not
        if self.lineedit_vertex.text() and self.lineedit_vertex.text().strip():
            self.pb_add_vertex.setDisabled(False)
        else:
            self.pb_add_vertex.setDisabled(True)

    def check_edge(self): # check edges if vertex is not eqal to itself and if vertex exist and if it is not whitespace
        if self.lineedit_edge_one.text() and self.lineedit_edge_one.text().strip() and self.lineedit_edge_two.text() and self.lineedit_edge_two.text().strip():
            self.pb_add_edge.setDisabled(False)
        else:
            self.pb_add_edge.setDisabled(True)

    def check_bfs(self): # check lineedit of bfs if empty or not
        if self.lineedit_bfs.text() and self.lineedit_bfs.text().strip():
            self.pb_bfs.setDisabled(False)
        else:
            self.pb_bfs.setDisabled(True)

    def check_dfs(self): # check lineedit of dfs if empty or not
        if self.lineedit_dfs.text() and self.lineedit_dfs.text().strip():
            self.pb_dfs.setDisabled(False)
        else:
            self.pb_dfs.setDisabled(True)

    def addVertex(self, vertex): # add vertex to graph
        # if vertex is not exist to graph
        # add vertex
        if vertex not in self.graph:
            self.graph[vertex] = []

    def addEdge(self, edge): # add edge to vertex
        # if vertex exist in graph add edge
        # else raise error
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.graph:
            self.graph[vertex1].append(vertex2)
        else:
            self.graph[vertex1] = [vertex2]

    def print_truth_table(self): # display thruth table 1 = true, 0 = false
        self.listWidget.clear()
        if self.index_vertex == 0:
            self.listWidget.addItem('Nothing to Show (Edge Truth Table)')
        else:
            length = len(self.vertex_list)
            indexing = 0
            format = ('{}\t' * length)
            tab = ('\t')
            self.listWidget.addItem(tab + format.format(*self.vertex_list) + '\n')
            for i in range(len(self.vertex_list)):
                self.listWidget.addItem(self.vertex_list[indexing] + tab + format.format(*self.status[indexing]) + '\n')
                indexing += 1

    def add_vertex(self):
        # this method is created for truth table purposes
        # following codes needs concentration and strong analization to understand
        new_vertex = self.lineedit_vertex.text().lstrip()
        bool = (new_vertex.isalpha())
        if new_vertex in self.vertex_list and bool == True:
            self.msg.setText("'" + new_vertex + "'" + ' is already in the Vertices!')
            x = self.msg.exec_()
            self.lineedit_vertex.clear()
        if bool == False:
            self.msg.setText("'" + new_vertex + "'" + ' is not an alphabet!')
            x = self.msg.exec_()
            self.lineedit_vertex.clear()
        if new_vertex not in self.vertex_list and bool == True:
            if self.index_vertex == 0 and self.added_edge == 0:# the first input of vertex will fall here
                self.vertex_list.insert(self.index_vertex, new_vertex)
                #status = [] # intializing the status to be empty so that the value will be right
                #empty_status = []
                for i in range(len(self.vertex_list)):# creating a status defending on the len of vertices
                    self.empty_status.insert(i, 0)

                for x in range(len(self.vertex_list)):
                    self.status.insert(x, self.empty_status)

                self.lineedit_vertex.clear()
                self.listWidget.clear()
                self.listWidget_2.clear()
                self.rb_show_ttb.setChecked(True)

                length = len(self.vertex_list)
                indexing = 0
                format = ('{}\t' * length)
                tab = ('\t')
                self.listWidget.addItem(tab + format.format(*self.vertex_list) + '\n')
                for i in range(len(self.vertex_list)):
                    self.listWidget.addItem(self.vertex_list[indexing] + tab + format.format(*self.status[indexing]) + '\n')
                    indexing += 1

                for x in range(len(self.vertex_list)):
                    self.listWidget_2.addItem('Vertex --> ' + self.vertex_list[x])

            if self.index_vertex > 0 and self.added_edge == 0: # if the user just continue to add vertex and never add edges (dealing in status)
                # we will insert a 0 in storage_list beacause the vertex is added
                self.vertex_list.insert(self.index_vertex, new_vertex)

                lenn = len(self.vertex_list)
                new = [] # a empty_status for a new inserted vertex
                for x in range(lenn - 1): # inserting 0 to new, - 1 because we will insert the last zero together with the other empty_status
                    new.insert(x, 0)

                i = self.vertex_list.index(new_vertex) # getting the index of a new added vertex so that we can insert the new there at the right index
                self.status.insert(i, new)

                for i in range(lenn):
                    
                    list__ = self.status[i]
                    list__.insert(lenn, 0)

                self.lineedit_vertex.clear()
                self.listWidget.clear()
                self.listWidget_2.clear()
                self.rb_show_ttb.setChecked(True)

                length = len(self.vertex_list)
                indexing = 0
                format = ('{}\t' * length)
                tab = ('\t')
                self.listWidget.addItem(tab + format.format(*self.vertex_list) + '\n')
                for i in range(len(self.vertex_list)):
                    self.listWidget.addItem(self.vertex_list[indexing] + tab + format.format(*self.status[indexing]) + '\n')
                    indexing += 1

                for x in range(len(self.vertex_list)):
                    self.listWidget_2.addItem('Vertex --> ' + self.vertex_list[x])

            if self.index_vertex > 0 and self.added_edge > 0: # if the user is already add edge (dealing in storage_list)
                # we will insert a 0 in storage_list beacause the vertex is added
                self.vertex_list.insert(self.index_vertex, new_vertex)

                lenn = len(self.vertex_list)
                new = [ ]# a empty_status for a new inserted vertex
                for x in range(lenn - 1): # inserting 0 to new, - 1 because we will insert the last zero together with the other empty_status
                    new.insert(x, 0)

                i = self.vertex_list.index(new_vertex)# getting the index of a new added vertex so that we can insert the new there at the right index
                self.storage_list.insert(i, new)

                for i in range(lenn):
                    list__ = self.storage_list[i]
                    list__.insert(lenn, 0)

                self.status = [] # clearing the status for updating
                self.status = self.storage_list # putting the content of storage_list in status

                self.lineedit_vertex.clear()
                self.listWidget.clear()
                self.listWidget_2.clear()
                self.rb_show_ttb.setChecked(True)

                length = len(self.vertex_list)
                indexing = 0
                format = ('{}\t' * length)
                tab = ('\t')
                self.listWidget.addItem(tab + format.format(*self.vertex_list) + '\n')
                for i in range(len(self.vertex_list)):
                    self.listWidget.addItem(self.vertex_list[indexing] + tab + format.format(*self.status[indexing]) + '\n')
                    indexing += 1

                for x in range(len(self.vertex_list)):
                    self.listWidget_2.addItem('Vertex --> ' + self.vertex_list[x])

            self.index_vertex += 1
            self.addVertex(new_vertex)
            if self.index_vertex > 0:
                self.pb_delete_all.setDisabled(False)

    def add_edge(self):
        # this method is created for truth table purposes
        # following codes needs concentration and strong analization to understand
        vertex_one = self.lineedit_edge_one.text()
        vertex_two = self.lineedit_edge_two.text()
        if vertex_one not in self.vertex_list:
            self.msg.setText('Please enter vertex that is in Vertices and should not be equal to each other.')
            y = self.msg.exec_()
            self.lineedit_edge_one.clear()
            self.lineedit_edge_two.clear()

        elif vertex_one and vertex_two in self.vertex_list and vertex_one != vertex_two:
            if self.added_edge == 0:  # because we cannot assign again the last value of status to the storage list
                self.storage_list = self.status  # [[0,0], [0,0]]

                index_one = self.vertex_list.index(vertex_one)  # getting the index value in vetex_list so that we can modify and access
                index_two = self.vertex_list.index(vertex_two)

                new_list_one = self.storage_list[index_one]  # putting the empty_status at this variable
                new_list_two = self.storage_list[index_two]

                len_one = len(new_list_one)
                len_two = len(new_list_one)
                new_list_one = []  # inializing to clear the list for inserting a new zero so that they will become new list
                new_list_two = []

                for i in range(len_one):  # creating/inserting a status 0 in the 2 list
                    new_list_one.insert(i, 0)

                for x in range(len_two):
                    new_list_two.insert(x, 0)

                del new_list_one[index_two]
                new_list_one.insert(index_two, 1)

                del new_list_two[index_one]
                new_list_two.insert(index_one, 1)

                del self.storage_list[index_one]
                self.storage_list.insert(index_one, new_list_one)

                del self.storage_list[index_two]
                self.storage_list.insert(index_two, new_list_two)
                self.status = self.storage_list  # passing again the value of storage_list to status so that it can be displayed

                self.lineedit_edge_one.clear()
                self.lineedit_edge_two.clear()
                self.listWidget.clear()
                self.rb_show_ttb.setChecked(True)

                length = len(self.vertex_list)
                indexing = 0
                format = ('{}\t' * length)
                tab = ('\t')
                self.listWidget.addItem(tab + format.format(*self.vertex_list) + '\n')
                for i in range(len(self.vertex_list)):
                    self.listWidget.addItem(self.vertex_list[indexing] + tab + format.format(*self.status[indexing]) + '\n')
                    indexing += 1

            if self.added_edge > 0:  # we will just modify the status in storage_list


                index_one = self.vertex_list.index(vertex_one)  # getting the index value in vetex_list so that we can modify and access
                index_two = self.vertex_list.index(vertex_two)

                new_list_one = self.storage_list[index_one]  # putting the empty_status at this variable
                new_list_two = self.storage_list[index_two]

                del new_list_one[index_two]
                new_list_one.insert(index_two, 1)

                del new_list_two[index_one]
                new_list_two.insert(index_one, 1)

                del self.storage_list[index_one]
                self.storage_list.insert(index_one, new_list_one)

                del self.storage_list[index_two]
                self.storage_list.insert(index_two, new_list_two)

                self.status = self.storage_list

                self.lineedit_edge_one.clear()
                self.lineedit_edge_two.clear()
                self.listWidget.clear()
                self.rb_show_ttb.setChecked(True)

                length = len(self.vertex_list)
                indexing = 0
                format = ('{}\t' * length)
                tab = ('\t')
                self.listWidget.addItem(tab + format.format(*self.vertex_list) + '\n')
                for i in range(len(self.vertex_list)):
                    self.listWidget.addItem(self.vertex_list[indexing] + tab + format.format(*self.status[indexing]) + '\n')
                    indexing += 1

            self.added_edge += 1
            self.addEdge({vertex_one, vertex_two})
            join = (vertex_one + vertex_two)
            self.edges.insert(self.i, join)
            self.i += 1

        else:
            self.msg.setText('Please enter vertex that is in Vertices and should not be equal to each other.')
            x = self.msg.exec_()
            self.lineedit_edge_one.clear()
            self.lineedit_edge_two.clear()

    def menu(self):
        # menu functionality
        current = self.comboBox.currentText()
        if current == 'Choose Action':
            self.container.show()
            self.BFS_container.hide()
            self.DFS_container.hide()
            self.add_vertex_container.hide()
            self.add_edge_container.hide()
            self.lineedit_vertex.clear()
            self.lineedit_edge_one.clear()
            self.lineedit_edge_two.clear()
            self.lineedit_bfs.clear()
            self.lineedit_dfs.clear()
        if current == 'Add Vertex':
            self.add_vertex_container.show()
            self.container.hide()
            self.BFS_container.hide()
            self.DFS_container.hide()
            self.add_edge_container.hide()
            self.lineedit_vertex.clear()
            self.lineedit_edge_one.clear()
            self.lineedit_edge_two.clear()
            self.lineedit_bfs.clear()
            self.lineedit_dfs.clear()
        if current == 'Add Edge':
            self.add_edge_container.show()
            self.container.hide()
            self.BFS_container.hide()
            self.DFS_container.hide()
            self.add_vertex_container.hide()
            self.lineedit_vertex.clear()
            self.lineedit_edge_one.clear()
            self.lineedit_edge_two.clear()
            self.lineedit_bfs.clear()
            self.lineedit_dfs.clear()
        if current == 'BFS Traversal':
            self.BFS_container.show()
            self.container.hide()
            self.DFS_container.hide()
            self.add_vertex_container.hide()
            self.add_edge_container.hide()
            self.lineedit_vertex.clear()
            self.lineedit_edge_one.clear()
            self.lineedit_edge_two.clear()
            self.lineedit_bfs.clear()
            self.lineedit_dfs.clear()
        if current == 'DFS Traversal':
            self.DFS_container.show()
            self.container.hide()
            self.BFS_container.hide()
            self.add_vertex_container.hide()
            self.add_edge_container.hide()
            self.lineedit_vertex.clear()
            self.lineedit_edge_one.clear()
            self.lineedit_edge_two.clear()
            self.lineedit_bfs.clear()
            self.lineedit_dfs.clear()

    def delete_all(self):
        # delete all data
        self.del_msg.setWindowTitle('Confirm Delete all')
        self.del_msg.setIcon(QMessageBox.Warning)
        self.del_msg.setText('Are you sure to delete all vertex?')
        self.del_msg.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        self.del_msg.setDefaultButton(QMessageBox.Cancel)
        y = self.del_msg.exec_()

    def action(self, i):
        if i.text() == '&Yes':
            self.neighbors = list()
            self.vertices = {}
            self.distance = 9999
            self.color = 'black'
            self.discovery = 0
            self.finish = 0
            self.time = 0

            self.listWidget.clear()
            self.listWidget_2.clear()
            self.listWidget_2.addItem('Nothing to show...')
            self.listWidget.addItem('Nothing to Show (Edge Truth Table)')
            self.rb_show_ttb.setChecked(True)
            self.pb_delete_all.setDisabled(True)
            self.index_vertex = 0  # index for vertex_list
            self.added_edge = 0  # when and edge is added it will increment
            self.indexing = 0
            self.i = 0
            self.edges = []
            self.vertex_list = []  # where vertex is inserted
            self.empty_status = []  # [0,0] to be inserted in status
            self.status = []  # [[0,0], [0,0]] the status of vertices
            self.storage_list = []  # where updated status is inserted and not to be edited

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pprint("Input parameters = " + str(sys.argv))
    iWindow = Ui_MainWindow()
    iWindow.show()
    sys.exit(app.exec_())



    CLIENT-3K






    
    1 - OK - 2 INPUTS, 3 OUTPUTS/   11  next/                       MP1 next/
    2 - OK - 1 INPUT, 1 OUTPUTS/    12  next/
    3 - OK - 2 INPUT, 1 OUTPUTS/    13  next
    4 - next/                       14  
    5 - OK - 3 INPUT, 1 OUTPUTS/    15
    6 - OK - 1 INPUT, 1 OUTPUTS/    16  next/
    7 - next/                       17  next/
    8 - next/                       18  next/
    9 - next/                       19 - OK - 1 INPUT, 1 OUTPUT/
    10 - next/                      20
