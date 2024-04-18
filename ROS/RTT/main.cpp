#include "rrt.h"

Node* RRT::GetNearestNode(const std::vector<double>& random_position) {
  int min_id = -1;
  double min_distance = std::numeric_limits<double>::max();
  for (int i = 0; i < node_list_.size(); i++) {
    double square_distance =
        std::pow(node_list_[i]->point().x - random_position[0], 2) +
        std::pow(node_list_[i]->point().y - random_position[1], 2);
    if (square_distance < min_distance) {
      min_distance = square_distance;
      min_id = i;
    }
  }

  return node_list_[min_id];
}

bool RRT::CollisionCheck(Node* newNode){//碰撞检测
   for(auto item:obstacle_list_){
     if(std::sqrt(std::pow(item[0]-newNode->point().x,2)+std::pow(item[1]-newNode->point().y,2))<=item[2]){
     	return false;
     }//与障碍物点的距离小于指定距离，视为撞上了
     
   }
   return true;
}

std::vector<Node*> RRT::Planning(){//关键的规划算法
   //显示的设置
   cv::namedWindow("RRT");
   int count=0;//不知道计算啥的数
   //显示背景设置
   constexpr int KImageSize=15;
   constexpr int kImageResolution=50;
   cv::Mat background(KImageSize* kImageResolution,KImageSize* kImageResolution,CV_8UC3,cv::Scalar(255,255,255));//定义背景图像矩阵
   //标出目标点和起始点
   circle(background,cv::Point(start_node_->point().x*  kImageResolution,start_node_->point().y* kImageResolution),20,cv::Scalar(0,0,255),-1);//红色圆
   circle(background,cv::Point(goal_node_->point().x* kImageResolution,goal_node_->point().y* kImageResolution),20,cv::Scalar(255,0,0),-1);
   //绘制黑色障碍物
   for (auto item:obstacle_list_){
   
   circle(background,cv::Point(item[0]* kImageResolution,item[1]* kImageResolution),20,cv::Scalar(0,0,0),-1);
   }
   //生长树迭代找路径
   node_list_.push_back(start_node_);
   while(1){  
    std::vector<double> random_position;
    //随机点生成
    if(goal_dis_(goal_len_)>goal_sample_rate_){//有两种概率，一种是在goal周围的概率，一个是在全局生成随机点的概率//两种概率组合
    					         //使生成点有概率在goal周围还有概率在全局周围，组合生成路径
       //采样在全局
       double randX=area_dis_(goal_len_);//这里貌似笔误了，不应该是area_gen_吗，但都是随机数种子无关大碍
       double randY=area_dis_(goal_len_);
       random_position.push_back(randX);
       random_position.push_back(randY);
    }
    else{//采样采到了goal
      random_position.push_back(goal_node_->point().x);
      random_position.push_back(goal_node_->point().y);
    }
   //找寻生成树中离随机点最近的点//生成两点间一步长的点加入到生长树里
   Node* nearestNode=GetNearestNode(random_position);
   double theta=atan2(random_position[1]-nearestNode->point().y,random_position[0]-nearestNode->point().x);
   Node* newNode=new Node(nearestNode->point().x+step_size_*cos(theta),nearestNode->point().y+step_size_*sin(theta));
   newNode->set_parent(nearestNode);
   if(!CollisionCheck(newNode)) continue;
   node_list_.push_back(newNode);
   //画图：画出线
   line(background,
         cv::Point(static_cast<int>(newNode->point().x *kImageResolution),
                   static_cast<int>(newNode->point().y *kImageResolution)),
         cv::Point(static_cast<int>(nearestNode->point().x * kImageResolution),
                   static_cast<int>(nearestNode->point().y * kImageResolution)),
         cv::Scalar(0, 255, 0), 10);
   //??
   count++;
   imshow("RRT",background);
   cv::waitKey(5);
   
   if(sqrt(pow(newNode->point().x-goal_node_->point().x,2)+pow(newNode->point().y-goal_node_->point().y,2))<=step_size_){
     std::cout<<"The path has been found!"<<std::endl;
     break;
   }
   } 
   //标出路径
   std::vector<Node*> path;
   path.push_back(goal_node_);
   Node* tmp_node=node_list_.back();//从后往前回溯
   while(tmp_node->parent()!=nullptr){
      line(
        background,
        
        cv::Point(static_cast<int>(tmp_node->point().x *kImageResolution),
                  static_cast<int>(tmp_node->point().y * kImageResolution)),
        cv::Point(
            static_cast<int>(tmp_node->parent()->point().x * kImageResolution),
            static_cast<int>(tmp_node->parent()->point().y * kImageResolution)),
        cv::Scalar(255, 0, 255), 10);
     path.push_back(tmp_node);
     tmp_node=tmp_node->parent();
   }
   //背景
   imshow("RRT",background);
   cv::waitKey(0);
   path.push_back(start_node_);
   return path;
}

int main(int argc, char* argv[]) {
  // (x, y, r)
  std::vector<std::vector<double>> obstacle_list{{7, 5, 1},  {5, 6, 2}, {5, 8, 2},
                                     {5, 10, 2}, {9, 5, 2}, {11, 5, 2}};

  Node* start_node = new Node(2.0, 2.0);
  Node* goal_node = new Node(14.0, 9.0);

  RRT rrt(start_node, goal_node, obstacle_list, 0.5, 5);
  rrt.Planning();
  return 0;
}
