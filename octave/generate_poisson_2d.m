function [samplepoints]=generate_poisson_2d(sz,min_dist,newpointscount)
  cellsize=min_dist/sqrt(2);
  grid=cell(ceil(sz(1)/cellsize),ceil(sz(2)/cellsize));
  proclist=[];
  samplepoints=[];

  firstpoint=ceil(sz.*rand(1,2));

  proclist=[proclist; firstpoint];

  samplepoints=[samplepoints; firstpoint];

  gridpoint=imageToGrid(firstpoint,cellsize);
  grid{gridpoint(1),gridpoint(2)}=firstpoint;

  while ~isempty(proclist)
      randrow=ceil(rand(1)*size(proclist,1));
      point=proclist(randrow,:);
      proclist(randrow,:)=[];
      
      for i=1:newpointscount
          disp(i)
          newpoint=generateRandomPointsAround(point, min_dist);
          if inRectangle(newpoint,sz) && ~inNeighbourhood(grid, newpoint, min_dist,cellsize)
              proclist=[proclist; newpoint];
              samplepoints=[samplepoints; newpoint];
              gridpoint=imageToGrid(newpoint,cellsize);
              grid{gridpoint(1),gridpoint(2)}=newpoint;
          end;
      end;
  end;


  figure(10);
  scatter(samplepoints(:,1),samplepoints(:,2));


end

function [gpoint]=imageToGrid(point,cellsize)
  gpoint=ceil(point/cellsize);
end

function [newpoint]=generateRandomPointsAround(point,min_dist)
  [x y z]=sph2cart(2*pi*rand(1),0,min_dist*(rand(1)+1));
newpoint=point+[x y];
end

function [isin]=inNeighbourhood(grid,point,min_dist,cellsize)
  gridsz=size(grid);
  gridpoint=imageToGrid(point,cellsize);
  [ox oy]=meshgrid(-2:2,-2:2); 
  c=repmat(gridpoint,[size(ox(:),1) 1])+[ox(:) oy(:)];
  c(any(c<1,2) | c(:,1)>gridsz(1) | c(:,2)>gridsz(2),:)=[];
  c(isempty(cat(1,grid{sub2ind(gridsz,c(:,1),c(:,2))})),:)=[];
  neighbour_points=cat(1,grid{sub2ind(gridsz,c(:,1),c(:,2))});
  if ~isempty(neighbour_points)
      dists=sqrt(sum((neighbour_points-repmat(point,[size(neighbour_points,1) 1])).^2,2));
      isin=any(dists<min_dist);
  else
      isin=false;
  end;
end

function [isin]=inRectangle(point,sz)
  isin=all(point>1) && all(point<=sz);
end
