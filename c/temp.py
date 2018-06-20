# include <stdio.h>
# include <stdlib.h>
# include <malloc.h>
# include <math.h>
# include <string.h>
# define SIZE 3//停车场最大车位数
// 1
为true，-1
为false

typedef
int
Status;

// 停在停车场中的车1
typedef
struct
CarPark
{
    char * snum; // 汽车车牌号
int
cartime; // 时间
}CarNode;
// 停车位结点
typedef
struct
{
    CarNode * base; // 堆栈底
CarNode * top; // 堆栈顶
int
stacksize;
}Park;
// 停在临时通道内的车
typedef
struct
CarLift
{
    char * snum; // 车号
int
cartime; // 到达时间
struct
CarLift * next;
}*CarPtr, CarNode2;
// 临时通道
typedef
struct
{
    CarPtr
front; // 队头
CarPtr
rear; // 尾
int
length;
}Shortcut;

// 初始化停车场
Status
InitStack(Park & P)
{
    P.base = (CarNode *)
malloc(SIZE * sizeof(CarPark));
if (!P.base)
exit(-1);
P.top = P.base;
P.stacksize = 0;
return 1;
}

// 车进入停车场
Status
Push(Park & P, CarNode
e)
{
*P.top + += e;
++P.stacksize;
return 1;
}

// 车离开停车场
Status
Pop(Park & P, CarNode & e)
{
if (P.top == P.base)
    printf("停车场没有车");
else
    {
        e = *--P.top;
    --P.stacksize;
    }
    return 1;
    }

    // 初始化临时通道
    Status
    InitQueue(Shortcut & S)
    {
    S.front = S.rear = (CarPtr)
    malloc(sizeof(CarLift));
    if (!S.front | | !S.rear)
    exit(-1);
    S.front->next = NULL;
    S.length = 0;
    return 1;
    }

    // 车进入临时通道
    Status
    EnQueue(Shortcut & S, char * snum, int
    cartime)
    {
    CarPtr
    p;
    p = (CarPtr)
    malloc(sizeof(CarLift));
    if (!p)
    exit(-1);
    p->snum = snum;
    p->cartime = cartime;
    p->next = NULL;
    S.rear->next = p;
    S.rear = p;
    ++S.length;
    return 1;
    }

    // 车离开临时通道，进入停车场
    Status
    DeQueue(Shortcut & S, CarPtr & w)
    {
    if (S.length == 0)
        printf("通道为空");
    else
        {
            w = S.front->next;
        S.front->next = w->next;
        --S.length;
        }
        return 1;
        }

        // 对进栈车辆的处理
        Status
        Arrival(Park & P, Shortcut & S)
        {
        char * carnum;
        carnum = (char *)
        malloc(10);
        int
        cartime;
        printf("请输入车牌号:");
        scanf("%s", carnum);
        printf("请输入进停车场的时间，以24进制，例如下午2:10写成1410:");
        scanf("%d", & cartime);
        if (P.stacksize < SIZE)
            {
                CarNode
            c;
            c.snum = (char *)
            malloc(10);
            c.snum = carnum;
            c.cartime = cartime;
            Push(P, c);
            printf("车牌为：%s的车停在第%d号位置\n", c.snum, P.stacksize);
            }
            else
            {
                EnQueue(S, carnum, cartime);
            printf("停车场已满，暂时停在便道的第%d个位置。\n", S.length);
            }
            return 1;
            }

            // 停车场的车离栈，同时计算车费；临时通道内的车进入停车场
            Status
            Leave(Park & P, Park & P1, Shortcut & S)
            {
            char * snum, flag = 1, money, cartime, cost_time, cost_hour, cost_min;
            int
            le_time;
            snum = (char *)
            malloc(10);
            printf("请输入离开车辆车牌号：");
            scanf("%s", snum);
            printf("请输入离开时间，例如1410：");
            scanf("%d", & le_time);
            CarNode
            e, m;
            CarPtr
            w;
            while (P.stacksize)
                {
                    Pop(P, e); // 车辆离开
                if (strcmp(e.snum, snum) == 0)
                {
                    flag = 0;
                cost_min = le_time % 100 - e.cartime % 100;
                cost_hour = le_time / 100 - e.cartime / 100;
                if (cost_min < 0){
                cost_hour -= 1;
                cost_min=60+cost_min;

                }


                money=cost_hour * 8+ceil(cost_min / 15.0) * 2; // 费用是小时数 * 8加上向上取整的分钟数以15分钟为计时单位
                cartime=e.cartime;
            break;
            }
            // 临时做个栈，然后将让道的车辆信息暂时存储在这个临时栈内
            Push(P1, e);
            }
            // 将临时栈内的信息插入停车场
            while (P1.stacksize)
                {
                    Pop(P1, e);
                Push(P, e);
                }
                // 汽车离开flag变为0，然后新车进入
                if (flag == 0)
                    {
                        printf("车牌为：%s已经离开停车场\n", e.snum);
                    if (S.length != 0)
                    {
                    DeQueue(S, w);
                    m.cartime=le_time; // 新进入的车的时间等于离开车的时间
                    m.snum=w->snum;
                    Push(P, m);
                    free(w);
                    printf("车牌号为%s的车已经由便道进入停车场\n", m.snum);
                    }

                    printf("停车费为%d，占用车位数为%d\n", money, P.stacksize);
                    }
                else
                    {
                        printf("停车场不存在车辆为%s的车", snum);
                }
                return 1;
                }

                // 展示停车场车辆的车牌号
                Status
                DisplayStack(Park
                p)
                {
                printf("停车场停车信息如下（先进的车辆在右边）：\n");
                if (p.base == NULL)
                    return -1;
                if (p.top == p.base)
                    printf("停车场中没有车");
                CarNode * q;
                q = p.top;
                while (q > p.base)
                    {
                        q - -;
                    printf("%s ", q->snum);
                    }
                    printf("\n");
                    return 1;
                    }
                    // 展示临时车道的车牌号
                    Status
                    DisplayQueue(Shortcut
                    s)
                    {
                    printf("便道停车信息如下（先进的车辆在右边）：\n");
                    if (s.front == s.rear)
                        printf("便道内没车");
                    CarPtr
                    p;
                    p = s.front->next;
                    while (p)
                        {
                            printf("%s ", p->snum);
                        p = p->next;
                        }
                        printf("\n");
                        return 1;
                        }

                        //
                        int
                        main()
                        {
                        int
                        m = 1;
                        char
                        flag; // 选项
                        Park
                        P, Q;
                        Shortcut
                        S;
                        InitStack(P);
                        InitStack(Q);
                        InitQueue(S);
                        while (m)
                            {
                                printf("-----------欢迎使用停车管理系统------------\n");
                            printf("1 汽车进车场\n");
                            printf("2 查看停车场和便道信息\n");
                            printf("3 汽车出车场\n");
                            printf("4 退出程序\n");
                            printf("请选择(1,2,3,4): ");
                            scanf("%c", & flag);
                            switch(flag)
                            {
                                case
                            '1':
                            Arrival(P, S);
                        break; // 车进入停车场
                        case
                        '2':
                        // 查看停车信息
                        DisplayStack(P);
                        DisplayQueue(S);
                        break;
                        case
                        '3':
                        Leave(P, Q, S);
                        break; // 车离开停车场
                        case
                        '4':
                        m = 0;
                        break; // 退出程序
                        default:
                        printf("Input error!\n");
                        break;
                        }
                        while (flag != '\n')
                            scanf("%c", & flag);
                            }
                            return 0;
                        }