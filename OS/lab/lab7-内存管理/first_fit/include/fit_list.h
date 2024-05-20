#ifndef FIT_LIST_H
#define FIT_LIST_H
struct Fit_ListItem
{
    int begin_address; //空闲孔开始地址
    int size; //空闲孔的大小
    int is_allocate;
    Fit_ListItem *previous;
    Fit_ListItem *next;
};

class Fit_List
{
public:
    Fit_ListItem* head;
public:
    // 初始化List
    Fit_List();
    // 显式初始化List
    void initialize();
    // 返回List元素个数
    int size();
    // 返回List是否为空
    bool empty();
    // 返回指向List最后一个元素的指针
    // 若没有，则返回nullptr
    Fit_ListItem *back();
    // 将一个元素加入到List的结尾
    void push_back(Fit_ListItem *itemPtr);
    // 删除List最后一个元素
    void pop_back();
    // 返回指向List第一个元素的指针
    // 若没有，则返回nullptr
    Fit_ListItem *front();
    // 将一个元素加入到List的头部
    void push_front(Fit_ListItem *itemPtr);
    // 删除List第一个元素
    void pop_front();
    // 分配元素
    int allocate(int size);//返回地址
    // 删除pos位置处的元素
    void erase(int pos);
    void erase(Fit_ListItem *itemPtr);
    // 返回指向pos位置处的元素的指针
    Fit_ListItem *at(int pos);
    // 返回给定第一个容纳下需要大小的位置
    Fit_ListItem* find_fit(int size);
    void release(int start_address,int size);
    Fit_ListItem* find_release(int start_address);
    void print_allocate();
    Fit_ListItem* find_hole();
};

#endif