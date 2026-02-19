from django.shortcuts import render, redirect
from django.db.models import Max
from .models import AirportNode
from .forms import AirportRouteForm, SearchNthNodeForm, ShortestPathForm

# Dashboard: Display all nodes and find the node with the maximum duration (Question 2)
def index(request):
    nodes = AirportNode.objects.all()
    
    # Question 2: Find the Longest Node based on duration
    longest_node = AirportNode.objects.order_by('-duration').first()
    
    context = {
        'nodes': nodes,
        'longest_node': longest_node,
    }
    return render(request, 'routes/index.html', context)

# Form handling to add new routes (Mandatory Instruction)
def add_route(request):
    if request.method == 'POST':
        form = AirportRouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AirportRouteForm()
    return render(request, 'routes/add_route.html', {'form': form})

# Search Function: Traverse N nodes in a specific direction (Question 1)
def search_nth(request):
    result = None
    search_path = []
    if request.method == 'POST':
        form = SearchNthNodeForm(request.POST)
        if form.is_valid():
            start_node = form.cleaned_data['start_airport']
            n = form.cleaned_data['n']
            direction = form.cleaned_data['direction']
            
            # Step-by-step traversal logic
            current = start_node
            search_path.append(current)
            for i in range(n):
                child = current.children.filter(position=direction).first()
                if child:
                    current = child
                    search_path.append(current)
                else:
                    current = None
                    break
            result = current
    else:
        form = SearchNthNodeForm()
    
    return render(request, 'routes/search_nth.html', {
        'form': form, 
        'result': result, 
        'search_path': search_path
    })

# Path-finding: Find the duration-weighted path between two airports (Question 3)
def shortest_path_view(request):
    path = None
    total_duration = 0
    if request.method == 'POST':
        form = ShortestPathForm(request.POST)
        if form.is_valid():
            from_node = form.cleaned_data['from_airport']
            to_node = form.cleaned_data['to_airport']
            
            # Algorithm: Find Least Common Ancestor (LCA) to determine the unique path in the tree
            def get_ancestors(node):
                ancestors = {}
                curr = node
                dist = 0
                while curr:
                    ancestors[curr.id] = (curr, dist)
                    curr = curr.parent
                    dist += 1
                return ancestors

            from_ancestors = get_ancestors(from_node)
            to_curr = to_node
            lca = None
            while to_curr:
                if to_curr.id in from_ancestors:
                    lca = to_curr
                    break
                to_curr = to_curr.parent
            
            if lca:
                # Build path from start to LCA
                path_from = []
                curr = from_node
                while curr.id != lca.id:
                    path_from.append(curr)
                    curr = curr.parent
                
                # Build path from LCA to destination
                path_to = []
                curr = to_node
                while curr.id != lca.id:
                    path_to.append(curr)
                    curr = curr.parent
                path_to.reverse()
                
                path = path_from + [lca] + path_to
                
                # Calculate total journey duration based on edge weights (node.duration)
                total_duration = 0
                for i in range(len(path) - 1):
                    u = path[i]
                    v = path[i+1]
                    if v.parent == u:
                        # Case: Moving down from parent to child
                        total_duration += v.duration
                    else:
                        # Case: Moving up from child to parent (reversing the edge)
                        total_duration += u.duration

    else:
        form = ShortestPathForm()
    
    return render(request, 'routes/shortest_path.html', {
        'form': form, 
        'path': path, 
        'total_duration': total_duration
    })
